from aiohttp.web import Application
from typing import Dict
from asyncio import Task


async def setup_search_tasks(app: Application):
    app['search_tasks']: Dict[str, Task] = {}

    yield

    try:
        tasks: Dict[str, Task] = app['search_tasks']
        for _, task in tasks.values():
            if not task.done():
                task.cancel()
            await task
    except Exception:
        pass
