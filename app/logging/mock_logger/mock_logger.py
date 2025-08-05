from typing import Any
from app.logging.ilogger import ILogger


class MockLogger(ILogger):
    def __init__(self) -> None:
        self.logs: list[tuple[str, str, dict[str, Any]]] = []

    def _record(self, level: str, message: str, **kwargs: Any) -> None:
        self.logs.append((level, message, kwargs))

    def info(self, message: str, **kwargs: Any) -> None:
        self._record("info", message, **kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        self._record("warning", message, **kwargs)

    def error(self, message: str, **kwargs: Any) -> None:
        self._record("error", message, **kwargs)

    def debug(self, message: str, **kwargs: Any) -> None:
        self._record("debug", message, **kwargs)

