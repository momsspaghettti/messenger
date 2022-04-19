import argparse
import os
from aiohttp.web import run_app
from messenger.create_app import create_app
from configargparse import ArgumentParser
from yarl import URL
from messenger.utils import DB_URL_TPL

parser = ArgumentParser(allow_abbrev=False, formatter_class=argparse.ArgumentDefaultsHelpFormatter)

group = parser.add_argument_group('API Options')
group.add_argument('--api-address', default='0.0.0.0',
                   help='IPv4/IPv6 address API server would listen on')
group.add_argument('--api-port', type=int, default=8080,
                   help='TCP port API server would listen on')

group = parser.add_argument_group('Database options')
group.add_argument('--db-url', type=URL, default=URL(os.getenv('DATABASE_URL', '')),
                   help='URL to use to connect to the database')

group.add_argument('--postgres-host', type=str, default=os.getenv('POSTGRES_HOSTS', '192.168.6.131').split(',')[-1],
                   help='PostgreSQL host')
group.add_argument('--postgres-db', type=str, default=os.getenv('POSTGRES_DB', 'messenger'),
                   help='PostgreSQL database')
group.add_argument('--postgres-user', type=str, default=os.getenv('POSTGRES_USER', 'messenger-api'),
                   help='PostgreSQL user')
group.add_argument('--postgres-pwd', type=str, default=os.getenv('POSTGRES_PWD', 'mk9I9Cm3mfOCMPXwVbubttOCOWc934'),
                   help='PostgreSQL password')

group.add_argument('--db-pool-min-size', type=int, default=10,
                   help='Minimum database connections')
group.add_argument('--db-pool-max-size', type=int, default=20,
                   help='Maximum database connections')


def main():
    args = parser.parse_args()

    args.db_url = DB_URL_TPL.format(
        args.postgres_user,
        args.postgres_pwd,
        args.postgres_host,
        args.postgres_db)

    app = create_app(args)
    run_app(app, host=args.api_address, port=args.api_port)


if __name__ == '__main__':
    main()
