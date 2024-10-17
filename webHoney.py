# Libraries
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request, flash, redirect
import requests

# Logging Format
logging_format = logging.Formatter('%(asctime)s %(message)s')

# HTTP logger
funnel_logger = logging.getLogger('HTTP Logger')
funnel_logger.setLevel(logging.INFO)
funnel_handler = RotatingFileHandler("HTTP_audits.log", maxBytes=1000, backupCount=5)
funnel_handler.setFormatter(logging_format)
funnel_logger.addHandler(funnel_handler)

def get_client_ip():
    if request.headers.get('X-Forwarded-For'):
        ip = request.headers['X-Forwarded-For'].split(',')[0].strip()
    else:
        ip = request.remote_addr
    return ip

def get_router_location(public_ip):
    try:
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

    app.config['SECRET_KEY'] = "Just a secret key"

    @app.route('/')
    def index():
        private_ip = get_client_ip()
        public_ip = requests.get("https://api.ipify.org").text  # Get the public IP of the server
        
        city, region, country, loc = get_router_location(public_ip)

        funnel_logger.info(f"Visitor Private IP: {private_ip}, Router Location: {city}, {region}, {country}, {loc}")

        return render_template("wb_admin.html")

    @app.route('/wb-admin-login', methods=['POST'])
    def login():
        username = request.form['username']
        password = request.form['password']
        
        private_ip = get_client_ip()
        
        public_ip = requests.get("https://api.ipify.org").text  # Get the public IP of the server
        
        city, region, country, loc = get_router_location(public_ip)

        funnel_logger.info(f"Login attempt from Private IP: {private_ip}, Router Location: {city}, {region}, {country}, {loc} "
                           f"with username: {username}, password: {password}")

        if username == input_username and password == input_password:
            return "Welcome"
        else:
            flash("Invalid credentials")
            return redirect('/')
        
    return app

def run_web_honeypot(input_username="admin", input_password="password"):
    run_web_pot = web_honeypot(input_username, input_password)
    run_web_pot.run(port=5500, debug=True, host="0.0.0.0")    

    return run_web_pot

if __name__ == "__main__":
    run_web_honeypot("admin", "password")
