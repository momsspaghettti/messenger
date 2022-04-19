import os
from messenger.utils import DB_URL_TPL
import uuid
from sqlalchemy_utils import create_database, drop_database
from aiopg.sa import create_engine
import pytest
from aiohttp.web import Application
from types import SimpleNamespace
from messenger.utils.db import setup_db
from messenger.utils.log import setup_logger_factory
from messenger.utils.messages_cache import MessagesCache
from configargparse import Namespace
from functools import partial
from messenger.utils.search_tasks import setup_search_tasks
from messenger.utils.alembic.alembic_config import make_alembic_config
from alembic.command import upgrade
from messenger.api.handlers.base import Handler
from typing import List, Type

POSTGRES_USER = os.getenv('POSTGRES_USER', 'messenger-api')
POSTGRES_HOST = os.getenv('POSTGRES_HOSTS', '192.168.6.131').split(',')[-1]
POSTGRES_PWD = os.getenv('POSTGRES_PWD', 'mk9I9Cm3mfOCMPXwVbubttOCOWc934')


@pytest.fixture
def create_app(test_client, args):
    def app_wrapper(handlers: List[Type[Handler]], with_db: bool = True):
        def create_app(loop):
            app = Application(loop=loop)
            add_ctx(app, args, with_db)
            add_handlers(app, handlers)
            return app

        return test_client(create_app)

    return app_wrapper


def add_ctx(app: Application, args, with_db: bool):
    if not with_db:
        args.db_url = ''

    app['args'] = args
    app['messages_cache'] = MessagesCache()

    app.cleanup_ctx.append(setup_logger_factory)
    app.cleanup_ctx.append(partial(setup_db, args=args))
    app.cleanup_ctx.append(setup_search_tasks)


def add_handlers(app: Application, handlers: List[Type[Handler]]):
    for handler in handlers:
        app.router.add_route('*', handler.URL_PATH, handler)


@pytest.fixture
def args(migrated_db):
    return Namespace(
        db_url=migrated_db,
        db_pool_min_size=10,
        db_pool_max_size=20)


@pytest.fixture
def migrated_db(alembic_config, db):
    upgrade(alembic_config, 'head')
    return db


@pytest.fixture
def alembic_config(db):
    cmd_options = SimpleNamespace(
        config='alembic.ini',
        name='alembic',
        db_url=db,
        raiseerr=False,
        x=None)
    return make_alembic_config(cmd_options)


@pytest.fixture(scope='session')
def db():
    tmp_db_name = '_'.join([uuid.uuid4().hex, 'pytest'])
    db_url = DB_URL_TPL.format(POSTGRES_USER, POSTGRES_PWD, POSTGRES_HOST, tmp_db_name)

    create_database(db_url)

    try:
        yield db_url
    finally:
        drop_database(db_url)


async def test_db(db):
    async with create_engine(db) as engine:
        async with engine.acquire() as conn:
            i = 0
            async for row in conn.execute('SELECT 1'):
                assert row == (1,)
                i += 1
            assert i == 1
