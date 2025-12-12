import logging
import sys

def configure_logger(name="AnchorFrame", level=logging.INFO):
    """
    Sets up a standard console logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Check if handler exists to avoid duplicates
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    return logger

def get_logger(name="AnchorFrame"):
    return logging.getLogger(name)
