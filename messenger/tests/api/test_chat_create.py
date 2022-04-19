import pytest
from aiohttp.web import Application
from messenger.api.handlers.chat_create import ChatCreateView
from tests.user import (
    user, user_without_utc_offset, registered_user,
    user_for_login, logged_in_user, logged_in_user_headers
)
from tests.utils import random_str, get_random_str
from typing import Optional

URL = '/v1/chats'


@pytest.fixture
async def client(create_app):
    return await create_app([ChatCreateView])


@pytest.fixture
async def created_chat_id(create_app, logged_in_user_headers: dict):
    client = await create_app([ChatCreateView])

    res = await client.post(
        URL,
        json={'chat_name': random_str(1, 255)},
        headers=logged_in_user_headers)
    assert res.status == 201

    res_json = await res.json()
    assert 'chat_id' in res_json

    chat_id = res_json['chat_id']
    assert chat_id is not None
    assert isinstance(chat_id, str)
    assert chat_id != ''

    return chat_id


def test_chat_create_ok(created_chat_id):
    assert created_chat_id is not None
    assert isinstance(created_chat_id, str)
    assert created_chat_id != ''


@pytest.mark.parametrize('bad_chat_name', [None, '', get_random_str(256)])
async def test_chat_create_bad_params1(
        client: Application,
        logged_in_user_headers: dict,
        bad_chat_name: str):
    res = await client.post(
        URL,
        json={'chat_name': bad_chat_name},
        headers=logged_in_user_headers)
    assert res.status == 400


@pytest.mark.parametrize(
    'bad_json',
    [
        None,
        {},
        {'x': 'x'},
        {'chat_name': random_str(1, 255), 'x': 'x'}
    ])
async def test_chat_create_bad_params2(
        client: Application,
        logged_in_user_headers: dict,
        bad_json: Optional[dict]):
    res = await client.post(
        URL,
        json=bad_json,
        headers=logged_in_user_headers)
    assert res.status == 400
