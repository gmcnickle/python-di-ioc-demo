from dependency_injector import containers, providers
from app.service.hello_console_service import HelloConsoleService
from app.service.hello_web_service import HelloWebService
from app.service.hello_windows_service import HelloWindowsService
from app.service.iservice import IService
from app.logging.ilogger_factory import ILoggerFactory
from typing import cast

class AppContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    logger_factory: providers.Provider[ILoggerFactory] = cast(
        providers.Provider[ILoggerFactory],
        providers.Dependency()
    )

    main_logger = providers.Factory(
        lambda factory: factory.create_logger("main"),
        factory=logger_factory
    )


    # Dynamically selects the service implementation based on the value of `config.service_type`.
    # 
    # This uses providers.Selector to map string keys from the config (like "console", "web", "windows")
    # to their corresponding service factories. All implementations must conform to the IService interface
    # and accept a logger dependency.
    #
    # For example:
    #   config.service_type = "console" → HelloConsoleService(logger=main_logger)
    #   config.service_type = "web"     → HelloWebService(logger=main_logger)
    #   config.service_type = "windows" → HelloWindowsService(logger=main_logger)
    #
    # This allows you to swap service implementations via config without modifying the container.
    hello_service: providers.Provider[IService] = providers.Selector(
        config.service_type,
        console=providers.Factory(HelloConsoleService, logger=main_logger),
        web=providers.Factory(HelloWebService, logger=main_logger),
        windows=providers.Factory(HelloWindowsService, logger=main_logger)
    )
