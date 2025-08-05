from typing import Type
from app.logging.ilogger_factory import ILoggerFactory
from app.logging.struct_logger.struct_logger_factory import StructLoggerFactory
from app.logging.mock_logger.mock_logger_factory import MockLoggerFactory
from app.logging.seqlogger.seq_logger_factory import SeqLoggerFactory

LOGGER_REGISTRY: dict[str, Type[ILoggerFactory]] = {
    "structlog": StructLoggerFactory,
    "mocklog": MockLoggerFactory,
    "seqlog": SeqLoggerFactory
}

