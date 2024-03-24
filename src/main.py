from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config import settings
from src.database import create_db_and_tables
from src.public.api import api as public_api
from src.utils.logger import logger_config

logger = logger_config(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()

    logger.info("startup: triggered")

    yield

    logger.info("shutdown: triggered")



app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url="/",
    lifespan=lifespan,
)


app.include_router(public_api)
