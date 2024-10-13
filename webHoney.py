# webhoneypot file - Arpan

# Libraries
import logging 
from logging.handlers import RotatingFileHandler
from flask import Flask,render_template,redirect,request,url_for

# Logging Format
logging_format = logging.Formatter('%(asctime)s %(message)s')

# HTTP logger
funnel_logger = logging.getLogger('HTTP Logger')
funnel_logger.setLevel(logging.INFO)
funnel_handler = RotatingFileHandler("HTTP_audits.log",maxBytes=1000,backupCount=5)
funnel_handler.setFormatter(logging_format)
funnel_logger.addHandler(funnel_handler)

# Baseline Honeypot

def web_honeypot(input_username="admin",input_password="password"):
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template("wb_admin.html")

    @app.route('/wb-admin-login',methods=['POST'])
    def login():
        username = request.form['username']
        password = request.form['password']
        
        ip_address = request.remote_addr

        funnel_logger.info(f"Client with IP Address: {ip_address} entered username {username}, Password {password}")

        if username == input_username and password == input_password:
            return "Welcome"
        else:
            return "Invalid username or password"
        
    return app


def run_web_honeypot(input_username="admin",input_password="password"):
    run_web_pot = web_honeypot(input_username,input_password)
    run_web_pot.run(port=5500,debug=True,host="0.0.0.0")    

    return run_web_pot

if __name__ == "__main__":
    run_web_honeypot("admin","password")