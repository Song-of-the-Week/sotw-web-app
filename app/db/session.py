from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL

from app.shared.config import cfg


# Synchronous engine
# engine_url = URL.create(
#     cfg.DB_SCHEME,
#     username=cfg.DB_USER,
#     password=cfg.DB_PASSWORD,
#     host=cfg.DB_HOST,
#     port=cfg.DB_PORT,
#     database=cfg.DB_NAME,
#     connect_args={'ssl_ca': cfg.DB_CA_PATH},
# )

engine = create_engine(f"cockroachdb://{cfg.DB_USER}:{cfg.DB_PASSWORD}@{cfg.DB_HOST}:{cfg.DB_PORT}/{cfg.DB_NAME}?sslmode=verify-full")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Asynchronous engine
# engine_async_url = URL.create(
#     cfg.DB_ASYNC_SCHEME,
#     username=cfg.DB_USER,
#     password=cfg.DB_PASSWORD,
#     host=cfg.DB_HOST,
#     port=cfg.DB_PORT,
#     database=cfg.DB_NAME,
#     connect_args={'ssl_ca': cfg.DB_CA_PATH},
# )
async_engine = create_async_engine(f"cockroachdb://{cfg.DB_USER}:{cfg.DB_PASSWORD}@{cfg.DB_HOST}:{cfg.DB_PORT}/{cfg.DB_NAME}?sslmode=verify-full")
AsyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=async_engine)
