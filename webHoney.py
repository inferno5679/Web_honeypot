# Libraries
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request
import requests

# Logging Format
logging_format = logging.Formatter('%(asctime)s %(message)s')

# HTTP logger
funnel_logger = logging.getLogger('HTTP Logger')
funnel_logger.setLevel(logging.INFO)
funnel_handler = RotatingFileHandler("HTTP_audits.log", maxBytes=1000, backupCount=5)
funnel_handler.setFormatter(logging_format)
funnel_logger.addHandler(funnel_handler)

# Function to get client's IP address (handles public or private IPs)
def get_client_ip():
    if request.headers.get('X-Forwarded-For'):
        # Use X-Forwarded-For header if present
        ip = request.headers['X-Forwarded-For'].split(',')[0].strip()
    else:
        # Fallback to remote address
        ip = request.remote_addr
    return ip

# Function to get location based on public IP address
def get_router_location(public_ip):
    try:
        # You can replace this with another geolocation API if you prefer
        response = requests.get(f"https://ipinfo.io/{public_ip}/json")
        if response.status_code == 200:
            data = response.json()
            return data.get("city"), data.get("region"), data.get("country"), data.get("loc")
    except requests.RequestException as e:
        funnel_logger.error(f"Error fetching location for {public_ip}: {e}")
    return None, None, None, None

# Baseline Honeypot
def web_honeypot(input_username="admin", input_password="password"):
    app = Flask(__name__)

    @app.route('/')
    def index():
        # Get client's IP address (private or public)
        private_ip = get_client_ip()
        
        # Get the public IP address of the honeypot server
        public_ip = requests.get("https://api.ipify.org").text  # Get the public IP of the server
        
        # Fetch router location using the public IP address
        city, region, country, loc = get_router_location(public_ip)

        # Log the private IP address and router location
        funnel_logger.info(f"Visitor Private IP: {private_ip}, Router Location: {city}, {region}, {country}, {loc}")

        # Render the web admin login page
        return render_template("wb_admin.html")

    @app.route('/wb-admin-login', methods=['POST'])
    def login():
        username = request.form['username']
        password = request.form['password']
        
        # Get client's IP address (private or public)
        private_ip = get_client_ip()
        
        # Get the public IP address of the honeypot server
        public_ip = requests.get("https://api.ipify.org").text  # Get the public IP of the server
        
        # Fetch router location using the public IP address
        city, region, country, loc = get_router_location(public_ip)

        # Log login attempts with private IP and router location
        funnel_logger.info(f"Login attempt from Private IP: {private_ip}, Router Location: {city}, {region}, {country}, {loc} "
                           f"with username: {username}, password: {password}")

        if username == input_username and password == input_password:
            return "Welcome"
        else:
            return "Invalid username or password"
        
    return app

def run_web_honeypot(input_username="admin", input_password="password"):
    run_web_pot = web_honeypot(input_username, input_password)
    run_web_pot.run(port=5500, debug=True, host="0.0.0.0")    

    return run_web_pot

# if __name__ == "__main__":
#     run_web_honeypot("admin", "password")
