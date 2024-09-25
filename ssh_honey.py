# libraries
import logging
from logging.handlers import RotatingFileHandler

# Logging

logging_format = logging.Formatter('%(message)s')

funnel_logger = logging.getLogger('FunnelLogger')
funnel_logger.setLevel(logging.INFO)
funnel_handler = RotatingFileHandler("audits.log",maxBytes=1000,backupCount=5)
funnel_handler.setFormatter(logging_format)
funnel_logger.addHandler(funnel_handler)

# Emulated Shell - Arpan

# SSH-server + Sockets - wamiq

# Provision based honeypot - wamiq