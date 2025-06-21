import logging
import sys
from logging.handlers import TimedRotatingFileHandler

# Create logger instance
logger = logging.getLogger("StarWarsAPI")

def setup_logger():
    # Set the lowest level to capture all messages
    logger.setLevel(logging.DEBUG)  

    # Create console handler and set level to INFO
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # Create file handler and set level to DEBUG
    file_handler = TimedRotatingFileHandler('app.log', when='midnight', backupCount=7)
    file_handler.setLevel(logging.DEBUG)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Add formatter to handlers
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger 