from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL

from app.shared.config import cfg


# Synchronous engine
engine_url = URL.create(
    cfg.POSTGRES_SCHEME,
    username=cfg.POSTGRES_USER,
    password=cfg.POSTGRES_PASSWORD,
    host=cfg.POSTGRES_HOST,
    port=cfg.POSTGRES_PORT,
    database=cfg.POSTGRES_DB,
)
engine = create_engine(engine_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Asynchronous engine
engine_async_url = URL.create(
    cfg.POSTGRES_ASYNC_SCHEME,
    username=cfg.POSTGRES_USER,
    password=cfg.POSTGRES_PASSWORD,
    host=cfg.POSTGRES_HOST,
    port=cfg.POSTGRES_PORT,
    database=cfg.POSTGRES_DB,
)
async_engine = create_async_engine(engine_async_url)
AsyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=async_engine)
