import logging
import sys

from pydantic import validator
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
from typing import List
from typing import Optional
from typing import Union
from loguru import logger

from app.shared.logging import InterceptHandler


class Config(BaseSettings):

    ### GENERAL ###
    DEV: bool = True
    API_V1_STR: str = "/api/v1"
    SERVER_BIND: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    LOGGER_LEVEL: int = logging.INFO
    LOGGING_CONFIG: str = "/home/clarice/sotw-web-app/app/log_conf.yaml"
    DEBUG: bool = False
    SEND_REGISTRATION_EMAILS: bool = False

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 11520  # 8 days
    SESSION_COOKIE_EXPIRE_SECONDS: int = 86400  # 30 minutes
    JWT_SECRET: str = (
        "7f0a187153e8c67cd0ef1a27552803e61b0a7051b9d981c8bf41a031b72a74d1"  # use `openssl rand -hex 32` to generate
    )
    ALGORITHM: str = "HS256"

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:8080",
        "http://localhost:8000",
    ]

    BACKEND_CORS_ORIGIN_REGEX: Optional[str] = "http://localhost:8080/*"

    @validator("BACKEND_CORS_ORIGINS", pre=True)  # 3
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    ### DATABASE ###
    POSTGRES_SCHEME: str = "postgresql"
    POSTGRES_ASYNC_SCHEME: str = "postgresql+asyncpg"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_USER: str = "clarice"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "sotw"
    POSTGRES_PORT: int = 5432


def setup_app_logging(config: Config) -> None:
    """Prepare custom logging for our application."""
    LOGGERS = ("uvicorn.asgi", "uvicorn.access")
    logging.getLogger().handlers = [InterceptHandler()]
    for logger_name in LOGGERS:
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers = [InterceptHandler(level=config.LOGGER_LEVEL)]

    logger.configure(handlers=[{"sink": sys.stderr, "level": config.LOGGER_LEVEL}])


cfg = Config()
