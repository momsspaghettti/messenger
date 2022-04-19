import argparse
import os
from messenger.utils import DB_URL_TPL
from alembic.config import CommandLine
from types import SimpleNamespace
from typing import Union
from configargparse import Namespace


def build_options() -> (CommandLine, Union[Namespace, SimpleNamespace]):
    alembic = CommandLine()
    alembic.parser.formatter_class = argparse.ArgumentDefaultsHelpFormatter
    alembic.parser.add_argument(
        '--db-url', default=os.getenv('DATABASE_URL', ''),
        help='Database URL [env var: DATABASE_URL]'
    )

    alembic.parser.add_argument(
        '--postgres-host',
        type=str,
        default=os.getenv('POSTGRES_HOSTS', '192.168.6.131').split(',')[-1],
        help='PostgreSQL host')
    alembic.parser.add_argument(
        '--postgres-db',
        type=str,
        default=os.getenv('POSTGRES_DB', 'messenger'),
        help='PostgreSQL database')
    alembic.parser.add_argument(
        '--postgres-user',
        type=str,
        default=os.getenv('POSTGRES_USER', 'messenger-api'),
        help='PostgreSQL user')
    alembic.parser.add_argument(
        '--postgres-pwd',
        type=str,
        default=os.getenv('POSTGRES_PWD', 'mk9I9Cm3mfOCMPXwVbubttOCOWc934'),
        help='PostgreSQL password')

    options = alembic.parser.parse_args()

    options.db_url = DB_URL_TPL.format(
        options.postgres_user,
        options.postgres_pwd,
        options.postgres_host,
        options.postgres_db)

    return alembic, options
