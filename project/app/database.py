import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker
from . import models

SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL")
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = AsyncEngine(create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True, future=True
))

#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionAsync = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
Base = declarative_base()

async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(models.Base.metadata.drop_all)
        await conn.run_sync(models.Base.metadata.create_all)