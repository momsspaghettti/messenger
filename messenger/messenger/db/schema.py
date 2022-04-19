from sqlalchemy import (
    Column, CheckConstraint, BigInteger, SmallInteger,
    MetaData, String, Table, ForeignKey, Text
)

convention = {
    'all_column_names': lambda constraint, table: '_'.join([
        column.name for column in constraint.columns.values()
    ]),

    # Именование индексов
    'ix': 'ix__%(table_name)s__%(all_column_names)s',

    # Именование уникальных индексов
    'uq': 'uq__%(table_name)s__%(all_column_names)s',

    # Именование CHECK-constraint-ов
    'ck': 'ck__%(table_name)s__%(constraint_name)s',

    # Именование внешних ключей
    'fk': 'fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s',

    # Именование первичных ключей
    'pk': 'pk__%(table_name)s'
}

metadata = MetaData(naming_convention=convention)

global_users_table = Table(
    'global_users',
    metadata,
    Column('id', BigInteger, primary_key=True, autoincrement=True),
    Column('login', String(255), nullable=False, index=True, unique=True),
    Column('password_hash_sha512', String(128), nullable=False),
    Column('name', String(255), nullable=False),
    Column('utc_offset', SmallInteger, nullable=False, default=0),
    CheckConstraint('utc_offset >= -24 and utc_offset <= 24', name='utc_offset_check'),
    CheckConstraint('char_length(login) > 0', name='login_min_len_check'),
    CheckConstraint('char_length(name) > 0', name='name_min_len_check'),
    CheckConstraint('char_length(password_hash_sha512) = 128', name='password_hash_sha512_len_check')
)

users_sessions_table = Table(
    'users_sessions',
    metadata,
    Column('session_id', String(128), primary_key=True),
    Column('global_user_id', BigInteger, ForeignKey('global_users.id'), nullable=False, index=True),
    CheckConstraint('char_length(session_id) = 128', name='session_id_len_check')
)

chats_table = Table(
    'chats',
    metadata,
    Column('chat_id', BigInteger, primary_key=True, autoincrement=True),
    Column('chat_name', String(255), nullable=False),
    CheckConstraint('char_length(chat_name) > 0', name='chat_name_min_len_check')
)

chats_users_table = Table(
    'chats_users',
    metadata,
    Column('user_id', BigInteger, primary_key=True, autoincrement=True),
    Column('user_name', String(255), nullable=False),
    Column('chat_id', BigInteger, ForeignKey('chats.chat_id'), nullable=False, index=True),
    Column('global_user_id', BigInteger, ForeignKey('global_users.id', ondelete='CASCADE'), nullable=False, index=True),
    CheckConstraint('char_length(user_name) > 0', name='user_name_min_len_check'),
)

chats_messages_table = Table(
    'chats_messages',
    metadata,
    Column('message_id', BigInteger, primary_key=True, autoincrement=True),
    Column('msg', Text, nullable=False),
    Column('chat_id', BigInteger, ForeignKey('chats.chat_id', ondelete='CASCADE'), nullable=False, index=True),
    Column('from_chat_user', BigInteger, ForeignKey('chats_users.user_id'), nullable=False),
    CheckConstraint('char_length(msg) > 0', name='msg_min_len_check')
)
