# libraries
import logging
from logging.handlers import RotatingFileHandler
import paramiko
# Logging

logging_format = logging.Formatter('%(message)s')

funnel_logger = logging.getLogger('FunnelLogger')
funnel_logger.setLevel(logging.INFO)
funnel_handler = RotatingFileHandler("audits.log",maxBytes=1000,backupCount=5)
funnel_handler.setFormatter(logging_format)
funnel_logger.addHandler(funnel_handler)

# Emulated Shell - Arpan

# SSH-server + Sockets - Sureshkumar + wamiq

class Server(paramiko.ServerInterface):
    
    def __init__(self, client_ip, input_username=None, input_password=None):
        self.client = client_ip
        self.input_username = input_username
        self.input_password = input_password
    
    def check_channel_request(self, kind:str, chanid: int):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
    
    def get_allowed_auths(self):
        return 'password'    
    
    def check_auth_password(self, username, password):
        
        if self.input_username is not None and self.input_password is not None:
            if username == 'username' and password == 'password':
                return paramiko.AUTH_SUCCESSFUL
            else:
                return paramiko.AUTH_FAILED
    
    def check_channel_shell_request(self, channel):
        self.event.set()
        return True
    
    #making naother mode
    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True
    
    def check_channel_exec_request(self, channel, command):
        command = str(command)
        return True
    
    
# Provision based honeypot - wamiq