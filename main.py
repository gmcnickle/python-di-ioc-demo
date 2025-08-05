from typing import Any, cast
from app.container import AppContainer
from bootstrap import load_config, configure_logging


def main() -> None:
    # Load and validate configuration first
    config = load_config()

    # Configure logging *before* initializing the container
    logger_factory = configure_logging(config)
    bootstrap_logger = logger_factory.create_logger("bootstrap")
    bootstrap_logger.info("Logger factory configured successfully.")

    ## At this point, we have a valid configuration and a logger factory ready to use.
    # Log the configuration for debugging purposes
    bootstrap_logger.debug(f"Loaded configuration: {config}")

    # Create and configure the DI container
    container = AppContainer()
    container.config.from_dict(cast(dict[str, Any], config))
    container.logger_factory.override(logger_factory)

    # Continue startup
    bootstrap_logger.info(f"Running service type: {config.get('service_type', 'console')}")
    service = container.hello_service()
    service.run()

if __name__ == "__main__":
    main()
