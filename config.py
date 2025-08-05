from typing import TypedDict

class AppConfig(TypedDict):
    service_type: str
    available_services: list[str]
    logger_factory: str
    available_loggers: list[str]

