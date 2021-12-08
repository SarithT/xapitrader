import logging
from xapitrader.utils import time
from xapitrader import settings

if settings.DEBUG_LOG:
    FORMAT = '[%(asctime)-15s][%(threadName)s-%(thread)d][%(levelname)s][%(name)s][%(funcName)s:%(lineno)d] %(message)s'
    level = logging.DEBUG
else:
    level = logging.INFO
    FORMAT = '[%(asctime)-15s][%(threadName)s-%(thread)d][%(levelname)s][%(name)s] %(message)s'

logging.basicConfig(
    level = level,
    format=FORMAT)

# Log to file settings
filename = f'{str(time.now())}.log'
fileHandler = logging.FileHandler(filename)
fileHandler.setFormatter(logging.Formatter(FORMAT))
fileHandler.setLevel(level)

class Logger():
    _logger = logging.getLogger('xtraderapi')
    _logger.addHandler(fileHandler)

    @classmethod
    def debug(self, msg: str):
        self._logger.debug(msg)
    
    @classmethod
    def info(self, msg: str):
        self._logger.info(msg)

    @classmethod
    def warning(self, msg: str):
        self._logger.warning(msg)

    @classmethod
    def error(self, msg: str):
        self._logger.error(msg)



