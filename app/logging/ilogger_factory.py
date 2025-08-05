from typing import Protocol, runtime_checkable
from app.logging.ilogger import ILogger

@runtime_checkable
class ILoggerFactory(Protocol):
    def create_logger(self, name: str) -> ILogger: ...

