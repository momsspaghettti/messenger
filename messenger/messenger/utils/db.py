import logging
from aiohttp.web import Application
from aiopg.sa import create_engine
from psycopg2 import OperationalError
from aiopg.sa import Engine
from typing import Optional, List, AsyncGenerator, Union, Any
from configargparse import Namespace
from messenger.utils.alembic.alembic_config import make_alembic_config_
from alembic.command import upgrade


async def create_db(db_url: str, min_pool_size: int, max_pool_size: int) -> (Optional[Engine], bool):
    try:
        async with create_engine(db_url, minsize=min_pool_size, maxsize=max_pool_size) as engine:
            async with engine.acquire() as conn:
                i = 0
                async for row in conn.execute('SELECT 1'):
                    assert row == (1,)
                    i += 1
                assert i == 1
                yield engine, True
    except OperationalError:
        yield None, False


async def setup_db(app: Application, args: Namespace):
    logger: logging.Logger = app['logger_factory'].get_logger(__name__)

    app['cleanup_tasks']: List[AsyncGenerator[Union[tuple[Engine, bool], tuple[None, bool]], Any]] = []

    async for db, c in create_db(str(args.db_url), args.db_pool_min_size, args.db_pool_max_size):
        app['db'], connected = db, c
        if connected:
            logger.info(f'Connected to database. Pool: ({args.db_pool_min_size}, {args.db_pool_max_size})')
        else:
            logger.warning('Failed to connect to database')

        yield

    try:
        logger.info(f'Found {len(app["cleanup_tasks"])} tasks to clean up. Starting...')
        for task in app['cleanup_tasks']:
            async for _ in task:
                continue
    except Exception as ex:
        logger.exception(ex)
    finally:
        logger.info('Done')


async def is_db_available(app: Application) -> bool:
    if app['db'] is None:
        return await try_create_db(app)

    try:
        async with app['db'].acquire() as conn:
            i = 0
            async for row in conn.execute('SELECT 1'):
                assert row == (1,)
                i += 1
            assert i == 1
            return True
    except OperationalError:
        return False


async def try_create_db(app: Application) -> bool:
    args = app['args']
    create_async_generator = create_db(str(args.db_url), args.db_pool_min_size, args.db_pool_max_size)
    async for db, c in create_async_generator:
        app['db'], connected = db, c
        if connected and db is not None:
            app['cleanup_tasks'].append(create_async_generator)
            return True
        else:
            continue
    return False


async def run_migrations(_: Application):
    config = make_alembic_config_()
    upgrade(config, 'head')
    yield
