from fastapi import FastAPI
from app.logging.ilogger import ILogger
from app.service.iservice import IService   
import uvicorn

class HelloWebService(IService):
    def __init__(self, logger: ILogger):
        self._logger = logger
        self._app = FastAPI()
        self._app.get("/")(self.read_root)

    def read_root(self) -> dict[str, str]:
        self._logger.info("Received request at /")
        return {"message": "Hello from the web!"}

    @property
    def app(self) -> FastAPI:
        return self._app

    def run(self) -> None:
        self._logger.info("Starting FastAPI web service...")
        uvicorn.run(self._app, host="0.0.0.0", port=8000)
