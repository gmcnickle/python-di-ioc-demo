import logging
import structlog
import sys

from app.logging.ilogger import ILogger
from app.logging.ilogger_factory import ILoggerFactory
from app.logging.struct_logger.struct_logger import StructLogger

class StructLoggerFactory(ILoggerFactory):
    def __init__(self) -> None:
        self._configured = False

    def create_logger(self, name: str = "app") -> ILogger:
        if not self._configured:
            self._configure()

        return StructLogger(name)

    def _configure(self) -> None:
        if self._configured:
            return

        # Base Python logging config
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)

        # Console (human-readable)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter("%(message)s"))
        root_logger.addHandler(console_handler)

        # File (JSON)
        file_handler = logging.FileHandler("app.log", mode="a", encoding="utf-8")
        file_handler.setFormatter(logging.Formatter("%(message)s"))
        root_logger.addHandler(file_handler)

        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.dev.set_exc_info,
                structlog.processors.format_exc_info,
                structlog.stdlib.ProcessorFormatter.wrap_for_formatter,  # 👈️ magic that sends to Python's logging
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
            cache_logger_on_first_use=True,
        )


        self._configured = True

