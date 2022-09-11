"""
Домашнее задание №4
Асинхронная работа с сетью и бд

доработайте функцию main, по вызову которой будет выполняться полный цикл программы
(добавьте туда выполнение асинхронной функции async_main):
- создание таблиц (инициализация)
- загрузка пользователей и постов
    - загрузка пользователей и постов должна выполняться конкурентно (параллельно)
      при помощи asyncio.gather (https://docs.python.org/3/library/asyncio-task.html#running-tasks-concurrently)
- добавление пользователей и постов в базу данных
  (используйте полученные из запроса данные, передайте их в функцию для добавления в БД)
- закрытие соединения с БД
"""

import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from models import Base, User, Post, async_engine, Session
import jsonplaceholder_requests
from typing import List, Iterable
from sqlalchemy import select
from sqlalchemy.engine import Result


async def create_tables():
    async with async_engine.begin() as conn:
        print("todo: drop all")
        await conn.run_sync(Base.metadata.drop_all)
        print("todo: create all")
        await conn.run_sync(Base.metadata.create_all)


async def create_users(session: AsyncSession, users_data: dict) -> List[User]:
    users = [User(name=user['name'], username=user['username'], email=user['email']) for user in users_data]
    print("users to create:", users)
    session.add_all(users)
    print("created users", users)
    await session.commit()
    return users


async def create_posts(session: AsyncSession, posts_data: dict) -> List[Post]:
    posts = [Post(user_id=post['userId'], title=post['title'], body=post['body']) for post in posts_data]
    print("posts to create:", posts)
    session.add_all(posts)
    await session.commit()
    print("created posts", posts)
    return posts


async def get_user_by_post(session: AsyncSession, title: str) -> User | None:
    stmt = select(User).join(User.posts).where(Post.title == title)
    result: Result = await session.execute(stmt)
    user: User | None = result.scalar_one_or_none()
    print(f"found user by post_title '{title}' - ", user.name)
    return user


async def get_posts_by_user(session: AsyncSession, name: str) -> List[Post] | None:
    stmt = select(Post).join(Post.user).where(User.name == name)
    result: Result = await session.execute(stmt)
    posts: Iterable[Post] = result.scalars()
    print(f"found posts by user '{name}': ")
    n = 1
    for post in posts:
        print(f"{n}. {post.title}")
        n += 1
    return list(posts)


async def async_main():
    await create_tables()
    # async with async_session() as session:
    async with Session() as session:
        users_data, posts_data = await asyncio.gather(
            jsonplaceholder_requests.fetch_users_data(),
            jsonplaceholder_requests.fetch_posts_data()
        )
        await create_users(session, users_data)
        await create_posts(session, posts_data)

        await get_user_by_post(session, 'qui est esse')
        await get_posts_by_user(session, "Leanne Graham")


def main():
    asyncio.run(async_main())


if __name__ == '__main__':
    main()
