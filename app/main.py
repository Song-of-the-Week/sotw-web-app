from curses import use_default_colors
import sys
import time
import uvicorn
from fastapi import APIRouter
from fastapi import Depends
from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.shared.config import cfg
from app.shared.config import setup_app_logging
from app.api import deps
from app.api.api_v1 import api_router


setup_app_logging(config=cfg)
root_router = APIRouter()
app = FastAPI(
    title="Song of the Week API", openapi_url=f"{cfg.API_V1_STR}/openapi.json"
)

if cfg.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in cfg.BACKEND_CORS_ORIGINS],
        allow_origin_regex=cfg.BACKEND_CORS_ORIGIN_REGEX,
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
    return {"hello": "world"}

@root_router.get("/health", status_code=200)
def health(
    request: Request,
    session: Session = Depends(deps.get_session),
) -> dict:
    """
    Root GET
    """
    return {"health": "ok"}


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
    uvicorn.run(
        f"{__name__}:app",
        host=cfg.SERVER_BIND,
        port=cfg.SERVER_PORT,
        log_level=cfg.LOGGER_LEVEL,
        reload=cfg.DEBUG,
    )


if __name__ == "__main__":
    sys.exit(main())
