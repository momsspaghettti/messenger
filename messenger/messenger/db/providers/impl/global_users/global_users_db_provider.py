import logging
from typing import Optional, List
from messenger.db.providers.global_users_provider import GlobalUsersProvider
from messenger.models.common.global_user import GlobalUser
from messenger.db.schema import global_users_table as tbl
from aiopg.sa.engine import Engine
from messenger.utils.timer import Timer


class GlobalUsersDbProvider(GlobalUsersProvider):
    def __init__(self, db: Engine, logger: logging.Logger):
        self.db: Engine = db
        self.logger: logging.Logger = logger

    async def save_users(self, users: List[GlobalUser]) -> None:
        async with Timer(self.logger, f'saving global {len(users)} users'):
            async with self.db.acquire() as conn:
                await conn.execute(tbl.insert().values([
                    {
                        'login': user.login,
                        'name': user.name,
                        'utc_offset': user.utc_offset
                    } for user in users
                ]))

    async def get_user(self, login: str) -> Optional[GlobalUser]:
        async with Timer(self.logger, 'getting global user'):
            async with self.db.acquire() as conn:
                result = await conn.execute(tbl.select().where(tbl.c.login == login))
                if result.rowcount == 0:
                    return None
                return GlobalUser(
                    id_=result['id'],
                    login=result['login'],
                    name=result['name'],
                    utc_offset=result['utc_offset'])
