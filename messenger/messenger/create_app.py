from aiohttp.web_app import Application
from messenger.api.handlers import HANDLERS
from messenger.utils.db import setup_db, run_migrations
from messenger.utils.log import setup_logger_factory
from messenger.utils.messages_cache import MessagesCache
from configargparse import Namespace
from functools import partial
from messenger.utils.search_tasks import setup_search_tasks


def create_app(args: Namespace) -> Application:
    app = Application()

    app['args'] = args
    app['messages_cache'] = MessagesCache()

    app.cleanup_ctx.append(setup_logger_factory)
    app.cleanup_ctx.append(run_migrations)
    app.cleanup_ctx.append(partial(setup_db, args=args))
    app.cleanup_ctx.append(setup_search_tasks)

    for handler in HANDLERS:
        app.router.add_route('*', handler.URL_PATH, handler)

    return app
