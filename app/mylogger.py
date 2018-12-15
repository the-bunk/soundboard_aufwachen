import logging
import sys

############
# SETTINGS #
############
STREAMLEVEL = logging.DEBUG
FILELEVEL = logging.INFO
LEVEL = logging.DEBUG
# FORMAT = "[%(levelname)8s:%(name)s:%(filename)s:%(lineno)s - %(funcName)16s() ] %(message)s"
FORMAT = "[%(levelname)8s:%(filename)s:%(lineno)s - %(funcName)16s() ] %(message)s"
FILENAME = "programm.log"


formatter = logging.Formatter(FORMAT)
logger = logging.getLogger(__name__)  # create main logger
logger.setLevel(LEVEL)

# file_handler = logging.RotatingFileHandler(FILENAME, maxBytes=10000000, backupCount=4)
# file_handler.setFormatter(formatter)
# file_handler.setLevel(FILELEVEL)
# logger.addHandler(file_handler)

stream_handler = logging.StreamHandler(stream=sys.stdout)
stream_handler.setFormatter(formatter)
stream_handler.setLevel(STREAMLEVEL)
logger.addHandler(stream_handler)


logger.debug("log")
logger.info(__name__)
logger.warning("log")
logger.error("log")
logger.critical("log")
