import structlog
from typing import Any
from app.logging.ilogger import ILogger


class StructLogger(ILogger):
    def __init__(self, name: str = "app") -> None:
        self._logger = structlog.get_logger(name)

    def info(self, message: str, **kwargs: Any) -> None:
        self._logger.info(message, **kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        self._logger.warning(message, **kwargs)

    def error(self, message: str, **kwargs: Any) -> None:
        self._logger.error(message, **kwargs)

    def debug(self, message: str, **kwargs: Any) -> None:
        self._logger.debug(message, **kwargs)
