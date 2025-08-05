from app.logging.ilogger_factory import ILoggerFactory
from app.logging.ilogger import ILogger
from app.logging.mock_logger.mock_logger import MockLogger


class MockLoggerFactory(ILoggerFactory):
    def __init__(self) -> None:
        self._logger = MockLogger()

    def create_logger(self, name: str) -> ILogger:
        # All requests return the same mock logger (shared logs)
        return self._logger

    def get_mock(self) -> MockLogger:
        return self._logger
