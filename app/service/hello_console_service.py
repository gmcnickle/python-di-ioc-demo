from app.logging.ilogger import ILogger
from app.service.iservice import IService

class HelloConsoleService(IService):
    def __init__(self, logger: ILogger):
        self._logger = logger

    def run(self) -> None:
        self._logger.info("Hello from the console!")
