"""
создайте асинхронные функции для выполнения запросов к ресурсам (используйте aiohttp)
"""
# from loguru import logger
# import asyncio
import aiohttp

USERS_DATA_URL = "https://jsonplaceholder.typicode.com/users/"
POSTS_DATA_URL = "https://jsonplaceholder.typicode.com/posts/"


async def fetch_json(session: aiohttp.ClientSession, url: str) -> dict:
    async with session.get(url) as response:
        data = await response.json()
        return data


async def fetch_users_data() -> dict:
    async with aiohttp.ClientSession() as session:
        data: dict = await fetch_json(session, USERS_DATA_URL)
        return data


async def fetch_posts_data() -> dict:
    async with aiohttp.ClientSession() as session:
        data: dict = await fetch_json(session, POSTS_DATA_URL)
        return data

# def main():
#     logger.info("Start fetch data")
#     users_data = asyncio.run(fetch_users_data())
#     posts_data = asyncio.run(fetch_posts_data())
#     logger.info("Finish fetch users data with result {!r}", users_data)
#     logger.info("Finish fetch posts data with result {!r}", posts_data)
#     for element in users_data:
#         print(element['name'])
#
#
# if __name__ == '__main__':
#     main()
