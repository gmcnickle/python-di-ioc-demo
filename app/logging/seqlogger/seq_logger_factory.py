import seqlog  # type: ignore
from app.logging.ilogger import ILogger
from app.logging.ilogger_factory import ILoggerFactory
from app.logging.seqlogger.seq_logger import SeqLogger


class SeqLoggerFactory(ILoggerFactory):
    def __init__(self) -> None:
        self._configured = False

    def _configure(self) -> None:
        if self._configured:
            return

        seqlog.configure_from_dict({
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "human": {
                    "format": "%(asctime)s %(levelname)s %(name)s - %(message)s"
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": "DEBUG",
                    "formatter": "human",
                },
                "seq": {
                    "class": "seqlog.structured_logging.SeqLogHandler",
                    "level": "INFO",
                    "formatter": "human",  
                    "server_url": "http://localhost:5341",
                    "api_key": None
                }
            },
            "loggers": {
                "": {
                    "level": "DEBUG",
                    "handlers": ["console", "seq"]
                }
            }
        })

        self._configured = True

    def create_logger(self, name: str) -> ILogger:
        self._configure()
        return SeqLogger(name)
