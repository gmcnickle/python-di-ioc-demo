import logging
from typing import Any
from app.logging.ilogger import ILogger


class SeqLogger(ILogger):
    def __init__(self, name: str) -> None:
        self._logger = logging.getLogger(name)

    def info(self, message: str, **kwargs: Any) -> None:
        self._logger.info(message, extra=kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        self._logger.warning(message, extra=kwargs)

    def error(self, message: str, **kwargs: Any) -> None:
        self._logger.error(message, extra=kwargs)

    def debug(self, message: str, **kwargs: Any) -> None:
        self._logger.debug(message, extra=kwargs)
