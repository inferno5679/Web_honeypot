# libraries
import logging
from logging.handlers import RotatingFileHandler
import paramiko
import socket
# Logging

logging_format = logging.Formatter('%(message)s')

funnel_logger = logging.getLogger('FunnelLogger')
funnel_logger.setLevel(logging.INFO)
funnel_handler = RotatingFileHandler("audits.log",maxBytes=1000,backupCount=5)
funnel_handler.setFormatter(logging_format)
funnel_logger.addHandler(funnel_handler)

creds_logger = logging.getLogger('CredsLogger')
creds_logger.setLevel(logging.INFO)
creds_handler = RotatingFileHandler("cmd_audits.log",maxBytes=1000,backupCount=5)
creds_handler.setFormatter(logging_format)
creds_logger.addHandler(creds_handler)

# Emulated Shell - Arpan
def emulated_shell(channel,client_ip):
    channel.send(b'corporate-jumpbox2$') # $ indicates that user has standard permissions 
    command = b""
    while True:
        char = channel.recv(1)
        channel.send(char)

        if not char:
            channel.close()

        command += char
    
        if char == b'\r':
            if command.strip() == b'exit':
                response = b'\n GoodBye'
                channel.close()
            elif command.strip() == 'pwd':
                respnse = b'/usr/local/' + b'\r\n'
            elif command.strip() == b'whoami':
                respnse = b'\n' + b'user1' + b'\r\n'
            elif command.strip() == b'ls':
                respnse = b'\n' + b'jumbox1.conf' + b'\r\n'
            elif command.strip() == b'cat jumpbox1.conf':
                respnse = b'\n' + b'go to google.com' + b'\r\n'
            else:
                respnse = b'\n' + bytes(command.strip()) + b'\r\n'
        
        
        channel.send(response)
        channel.send(b"corporate-jumpbpx2$ ")
        command = b""

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
    
    #making another mode
    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True
    
    def check_channel_exec_request(self, channel, command):
        command = str(command)
        return True
    
    
# Provision based honeypot - wamiq