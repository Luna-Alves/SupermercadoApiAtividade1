import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger('supermercado_api')
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')


streamHandler = logging.StreamHandler()
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)


file_handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
