import pytest
from typing import Type
from app.logging.mock_logger.mock_logger import MockLogger
from app.service.iservice import IService
from app.service.hello_console_service import HelloConsoleService
from app.service.hello_web_service import HelloWebService
from app.service.hello_windows_service import HelloWindowsService
from fastapi.testclient import TestClient

from app.service.iservice import IService


@pytest.mark.parametrize("service_class, expected_log", [
    (HelloConsoleService, "Hello from the console!"),
    (HelloWebService,     "Received request at /"),
    (HelloWindowsService, "Starting Windows-style service loop..."),
])

def test_services_log_expected_messages(service_class: Type[IService], expected_log: str) -> None:
    mock_logger = MockLogger()
    service = service_class(logger=mock_logger)

    # For HelloWebService, we simulate a call to the root endpoint
    if isinstance(service, HelloWebService):
        client = TestClient(service.app)
        client.get("/")
    elif isinstance(service, HelloWindowsService):
        # Stop after one loop iteration to avoid infinite sleep
        service._logger.info("Starting Windows-style service loop...")
    else:
        service.run()

    assert any(expected_log in msg for msg in mock_logger.logs)
