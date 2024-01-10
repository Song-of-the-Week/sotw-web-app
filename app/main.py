import time
import logging
import uvicorn
import yaml
from fastapi import APIRouter
from fastapi import Depends
from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.shared.config import cfg
from app.api import deps
from app.api.api_v1 import api_router

logger = logging.getLogger(__name__)

root_router = APIRouter()
app = FastAPI(title="Song of the Week API", openapi_url=f'{cfg.API_V1_STR}/openapi.json')

if cfg.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in cfg.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@root_router.get("/", status_code=200)
def root(
    request: Request,
    session: Session = Depends(deps.get_session),
) -> dict:
    """
    Root GET
    """
    logger.error(request)
    return { 'hello': 'world' }


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.include_router(api_router, prefix=cfg.API_V1_STR)
app.include_router(root_router)


def main() -> None:
    # get logger config
    with open(cfg.LOGGING_CONFIG, 'r') as file:
        log_config = yaml.safe_load(file)
    uvicorn.run(
        f'{__name__}:app',
        host=cfg.SERVER_BIND,
        port=cfg.SERVER_PORT,
        log_config=log_config,
        log_level=cfg.LOGGER_LEVEL,
        access_log=False,
        reload=cfg.DEBUG,
        use_colors=True,
    )
