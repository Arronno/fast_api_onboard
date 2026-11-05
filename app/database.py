import uuid
import datetime

from fastapi import Depends
from collections.abc import AsyncGenerator
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from fastapi_users.db import SQLAlchemyUserDatabase, SQLAlchemyBaseOAuthAccountTableUUID


DATABASE_URL = "sqlite+aiosqlite:///./test.db"


class DCBase(DeclarativeBase):
    pass


class User(SQLAlchemyBaseOAuthAccountTableUUID, DCBase):
    posts = relationship(argument="Post", back_populates="user")


class Post(DCBase):
    __tablename__ = "posts"

    post_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # ForeignKey --> Reference to another table, One to Many, Child should have ForeignKey
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    caption = Column(Text)
    url = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))

    user = relationship(argument="User", back_populates="posts")


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


# Create DB & Tables
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(DCBase.metadata.create_all)


# Async Interact with DB
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session=session, user_table=User)
