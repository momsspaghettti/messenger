import pytest
from messenger.api.handlers.chat_messages import ChatMessagesView
from typing import Tuple, List, Any
from tests.user import (
    user, user_without_utc_offset, registered_user,
    user_for_login, logged_in_user, logged_in_user_headers
)
from tests.api.test_chat_create import created_chat_id
from tests.api.test_chat_join import chat_and_joined_user
from tests.api.test_chat_send_message import send_messages

URL = '/v1/chats/{}/messages'


@pytest.fixture
async def client(create_app):
    return await create_app([ChatMessagesView])


def build_url(chat_id: str, query_params: List[Tuple[str, Any]]):
    url = URL.format(chat_id)
    query = '&'.join(f'{key}={value}' for key, value in query_params)
    if query != '':
        url += '?' + query

    return url


@pytest.mark.parametrize(
    'messages_count,limit',
    [(20, 5), (20, 20), (5, 20), (20, 6), (20, 1), (1, 100)]
)
async def test_chat_get_messages_ok(
        client,
        logged_in_user_headers: dict,
        chat_and_joined_user: Tuple[str, str],
        send_messages,
        messages_count: int,
        limit: int):
    chat_id, _ = chat_and_joined_user

    await send_messages(messages_count)

    from_ = None
    got_messages_count = 0
    while True:
        query_params = [('limit', limit)]
        if from_ is not None:
            query_params.append(('from', from_))

        res = await client.get(
            build_url(chat_id, query_params),
            headers=logged_in_user_headers)
        assert res.status == 200

        res_json = await res.json()
        assert 'messages' in res_json
        messages = res_json['messages']
        assert len(messages) > 0
        got_messages_count += len(messages)

        for message in messages:
            assert 'text' in message
            text = message['text']
            assert text is not None
            assert isinstance(text, str)
            assert len(text) > 0

        assert 'next' in res_json
        next_ = res_json['next']
        if next_ is not None:
            assert 'iterator' in next_
            iterator = next_['iterator']
            assert iterator is not None
            assert isinstance(iterator, str)
            assert len(iterator) > 0

            from_ = iterator
        else:
            from_ = None

        if from_ is None:
            break

    assert got_messages_count == messages_count
