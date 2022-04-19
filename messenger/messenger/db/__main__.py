from messenger.utils.alembic.build_options import build_options
from messenger.utils.alembic.alembic_config import make_alembic_config


def main():
    alembic, options = build_options()

    if 'cmd' not in options:
        alembic.parser.error('too few arguments')
        exit(128)
    else:
        config = make_alembic_config(options)
        exit(alembic.run_cmd(config, options))


if __name__ == '__main__':
    main()
