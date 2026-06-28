import logging
import os

if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    filename="logs/application.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def log_info(msg):
    logging.info(msg)

def log_error(msg):
    logging.error(msg)

def log_warning(msg):
    logging.warning(msg)