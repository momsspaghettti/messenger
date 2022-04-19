import pytest
from aiohttp.web import Application
from messenger.api.handlers.chat_join import ChatJoinView
from tests.user import (
    user, user_without_utc_offset, registered_user,
    user_for_login, logged_in_user, logged_in_user_headers
)
from tests.utils import random_str, get_random_str
from tests.api.test_chat_create import created_chat_id

URL = '/v1/chats/{}/users'


@pytest.fixture
async def client(create_app):
    return await create_app([ChatJoinView])


@pytest.fixture
async def chat_and_joined_user(
        create_app,
        logged_in_user_headers: dict,
        created_chat_id: str):
    client = await create_app([ChatJoinView])

    res = await client.post(
        URL.format(created_chat_id),
        json={'user_name': random_str(1, 255)},
        headers=logged_in_user_headers)
    assert res.status == 201

    res_json = await res.json()
    assert 'user_id' in res_json
    user_id = res_json['user_id']
    assert user_id is not None
    assert isinstance(user_id, str)
    assert user_id != ''

    return created_chat_id, user_id


async def test_chat_join_ok(chat_and_joined_user):
    _, user_id = chat_and_joined_user
    assert user_id is not None
    assert isinstance(user_id, str)
    assert user_id != ''


async def test_chat_join_incorrect_chat_id_not_found(
        client: Application,
        logged_in_user_headers: dict):
    res = await client.post(
        URL.format('123'),
        json={'user_name': random_str(1, 255)},
        headers=logged_in_user_headers)
    assert res.status == 404
    res_json = await res.json()
    assert 'message' in res_json
    assert 'chat' in res_json['message']
