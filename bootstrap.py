from app.container_registries import LOGGER_REGISTRY
from app.logging.ilogger_factory import ILoggerFactory
from config import AppConfig
import json
import os
from typing import cast

def configure_logging(config: AppConfig) -> ILoggerFactory:
    factory_key = config.get("logger_factory", "")
    factory_builder = LOGGER_REGISTRY.get(factory_key)

    if not factory_builder:
        raise ValueError(f"Unknown logger factory: {factory_key}")

    logger_factory = factory_builder()
    bootstrap_logger = logger_factory.create_logger("bootstrap")
    bootstrap_logger.info(f"Using logger factory: {factory_key}")

    return logger_factory


# This code is not strictly necessary for the purposes of this demo, but I went ahead and added it
# to illustrate that not everything belongs in the container.  Injection Containers (IoCs) are meant to declare wiring and dependencies,
# not to perform validation or other logic that doesn't directly relate to dependency injection.
# This is a good example of where you might want to keep validation logic separate from the container itself.
# In this case, we validate the config before creating the container.
def validate_config(config: AppConfig) -> None:
    service_type = config.get("service_type", "")
    available_services = config.get("available_services", [])

    if service_type not in available_services:
        raise ValueError(
            f"Invalid service_type '{service_type}'. "
            f"Must be one of: {available_services}"
        )
    
    logger_factory_type = config.get("logger_factory", "")
    available_loggers = config.get("available_loggers", [])
    if logger_factory_type not in available_loggers:
        raise ValueError(
            f"Invalid logger_factory '{logger_factory_type}'. "
            f"Must be one of: {available_loggers}"
        )

def load_config() -> AppConfig:
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_path) as f:
        config = cast(AppConfig, json.load(f))

    validate_config(config)
    return config
