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
    """Logs simple general runtime milestones."""
    logging.info(msg)

def log_error(msg):
    """Logs system runtime crashes or database statement failures."""
    logging.error(msg)

def log_warning(msg):
    """Logs authentication rejections or input layout alerts."""
    logging.warning(msg)