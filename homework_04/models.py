"""
создайте алхимичный engine
добавьте declarative base (свяжите с engine)
создайте объект Session
добавьте модели User и Post, объявите поля:
для модели User обязательными являются name, username, email
для модели Post обязательными являются user_id, title, body
создайте связи relationship между моделями: User.posts и Post.user
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# from sqlalchemy.orm import declared_attr

DB_ASYNC_URL = "postgresql+asyncpg://username:passwd!@localhost:5432/blog"
DB_ECHO = False

async_engine: AsyncEngine = create_async_engine(DB_ASYNC_URL, echo=DB_ECHO)
Session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=False)
    username = Column(String(20), unique=True)
    email = Column(String(30), unique=True)

    posts = relationship("Post", back_populates="user", uselist=True)


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), unique=False, nullable=False)
    body = Column(Text, nullable=False, default=None)

    user = relationship("User", back_populates="posts")
