from messenger.db.schema import chats_table as chats_tbl
from messenger.db.schema import chats_users_table as chats_users_tbl
from aiopg.sa import SAConnection
from logging import Logger
from psycopg2.errors import InvalidTextRepresentation


def chat_exists_query(chat_id: str):
    return chats_tbl.select().where(chats_tbl.c.chat_id == chat_id)


async def check_if_chat_exists(conn: SAConnection, chat_id: str, logger: Logger) -> bool:
    chat_exists: bool
    try:
        chat_exists = (await conn.execute(
            chat_exists_query(chat_id)
        )).rowcount == 1
    except InvalidTextRepresentation:
        logger.warning(f'chat_id = {chat_id} does not exist')
        return False

    if not chat_exists:
        logger.warning(f'chat_id = {chat_id} does not exist')
        return False

    return True


def chat_user_exists_query(user_id: str, chat_id: str):
    return chats_users_tbl \
        .select() \
        .where(chats_users_tbl.c.user_id == user_id and
               chats_users_tbl.c.chat_id == chat_id)


async def check_if_chat_user_exists(
        conn: SAConnection,
        user_id: str,
        chat_id: str,
        logger: Logger) -> bool:
    chat_user_exists: bool
    try:
        chat_user_exists = (await conn.execute(
            chat_user_exists_query(user_id, chat_id)
        )).rowcount == 1
    except InvalidTextRepresentation:
        logger.warning(f'user_id = {user_id} does not exist in chat with chat_id = {chat_id}')
        return False

    if not chat_user_exists:
        logger.warning(f'user_id = {user_id} does not exist in chat with chat_id = {chat_id}')
        return False

    return True
