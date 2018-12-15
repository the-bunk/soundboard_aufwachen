import logging
import sys

############
# SETTINGS #
############
STREAMLEVEL = logging.DEBUG
FILELEVEL = logging.INFO
LEVEL = logging.DEBUG
FORMAT = "[%(levelname)8s:%(filename)s:%(lineno)s - %(funcName)16s() ] %(message)s"
FILENAME = "programm.log"


formatter = logging.Formatter(FORMAT)
logger = logging.getLogger(__name__)  # create main logger
logger.setLevel(LEVEL)

stream_handler = logging.StreamHandler(stream=sys.stdout)
stream_handler.setFormatter(formatter)
stream_handler.setLevel(STREAMLEVEL)
logger.addHandler(stream_handler)


logger.debug("log")
logger.info(__name__)
logger.warning("log")
logger.error("log")
logger.critical("log")
