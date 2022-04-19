import random

import pytest
from messenger.api.handlers.chat_messages import ChatMessagesView
from typing import Tuple, List
from tests.user import (
    user, user_without_utc_offset, registered_user,
    user_for_login, logged_in_user, logged_in_user_headers
)
from tests.utils import random_str, get_random_str
from tests.api.test_chat_create import created_chat_id
from tests.api.test_chat_join import chat_and_joined_user

URL = '/v1/chats/{}/messages'


@pytest.fixture
async def client(create_app):
    return await create_app([ChatMessagesView])


@pytest.fixture
async def send_messages(
        create_app,
        logged_in_user_headers: dict,
        chat_and_joined_user: Tuple[str, str]):
    client = await create_app([ChatMessagesView])

    chat_id, user_id = chat_and_joined_user

    async def wrapper(messages_count: int):
        sent: List[str] = []
        for _ in range(messages_count):
            res = await client.post(
                URL.format(chat_id),
                json={'user_id': user_id, 'message': random_str(1, 10000)},
                headers=logged_in_user_headers)
            assert res.status == 201

            res_json = await res.json()
            assert 'message_id' in res_json

            message_id = res_json['message_id']
            assert message_id is not None
            assert isinstance(message_id, str)
            assert len(message_id) > 0

            sent.append(message_id)

        assert len(sent) == messages_count
        return sent

    return wrapper


async def test_chat_send_message_ok(send_messages):
    await send_messages(1)
    assert True


@pytest.mark.parametrize(
    'incorrect_chat_id',
    ['123456', str(random.randint(-1000, 1000)), get_random_str(100)])
async def test_chat_send_incorrect_chat_id_not_found(
        client,
        logged_in_user_headers: dict,
        chat_and_joined_user: Tuple[str, str],
        incorrect_chat_id: str):
    _, user_id = chat_and_joined_user
    res = await client.post(
        URL.format(incorrect_chat_id),
        json={'user_id': user_id, 'message': random_str(1, 10000)},
        headers=logged_in_user_headers)
    assert res.status == 404
    res_json = await res.json()
    assert 'message' in res_json
    assert 'chat' in res_json['message']


@pytest.mark.parametrize(
    'incorrect_user_id',
    ['123456', str(random.randint(-1000, 1000)), get_random_str(100)])
async def test_chat_send_incorrect_user_id_not_found(
        client,
        logged_in_user_headers: dict,
        chat_and_joined_user: Tuple[str, str],
        incorrect_user_id: str):
    chat_id, _ = chat_and_joined_user
    res = await client.post(
        URL.format(chat_id),
        json={'user_id': incorrect_user_id, 'message': random_str(1, 10000)},
        headers=logged_in_user_headers)
    assert res.status == 404
    res_json = await res.json()
    assert 'message' in res_json
    assert 'user' in res_json['message']
