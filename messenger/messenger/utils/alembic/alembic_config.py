import os
from messenger.project_path import PROJECT_PATH
from types import SimpleNamespace
from typing import Union
from configargparse import Namespace
from alembic.config import Config
from .build_options import build_options


def make_alembic_config(
        cmd_options: Union[Namespace, SimpleNamespace],
        base_path: str = PROJECT_PATH) -> Config:
    if not os.path.isabs(cmd_options.config):
        cmd_options.config = os.path.join(base_path, cmd_options.config)

    config = Config(file_=cmd_options.config, ini_section=cmd_options.name,
                    cmd_opts=cmd_options)

    alembic_location = config.get_main_option('script_location')
    if not os.path.isabs(alembic_location):
        config.set_main_option('script_location',
                               os.path.join(base_path, alembic_location))
    if cmd_options.db_url:
        config.set_main_option('sqlalchemy.url', cmd_options.db_url)

    return config


def make_alembic_config_(base_path: str = PROJECT_PATH) -> Config:
    _, cmd_options = build_options()
    return make_alembic_config(cmd_options, base_path)
