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