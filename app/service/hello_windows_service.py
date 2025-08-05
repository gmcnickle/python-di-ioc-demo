import time

from app.logging.ilogger import ILogger
from app.service.iservice import IService   

class HelloWindowsService(IService):
    def __init__(self, logger: ILogger):
        self._logger = logger

    def run(self) -> None:
        self._logger.info("Starting Windows-style service loop...")
        try:
            while True:
                self._logger.info("Still running...")
                time.sleep(60)
        except KeyboardInterrupt:
            self._logger.info("Shutting down gracefully...")
