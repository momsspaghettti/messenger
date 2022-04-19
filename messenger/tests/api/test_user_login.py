import pytest
from aiohttp.web import Application
from messenger.api.handlers.user_login import UserLoginView
from tests.user import user, user_without_utc_offset, registered_user, user_for_login
from tests.utils import random_str

URL = '/v1/login'


@pytest.fixture
async def client(create_app):
    return await create_app([UserLoginView])


async def test_user_login_ok(client, user_for_login):
    res = await client.post(URL, json=user_for_login)
    assert res.status == 201

    res_json = await res.json()
    assert 'session_id' in res_json
    session_id = res_json['session_id']
    assert isinstance(session_id, str)
    assert len(session_id) == 128


async def test_user_login_many_time_same_session_id(client, user_for_login):
    res = await client.post(URL, json=user_for_login)
    assert res.status == 201

    res_json = await res.json()
    assert 'session_id' in res_json
    first_session_id = res_json['session_id']
    assert isinstance(first_session_id, str)
    assert len(first_session_id) == 128

    for _ in range(5):
        res = await client.post(URL, json=user_for_login)

        assert res.status == 201

        res_json = await res.json()
        assert 'session_id' in res_json
        assert res_json['session_id'] == first_session_id


async def test_user_incorrect_login_not_found(client, user_for_login: dict):
    user_for_login['login'] = random_str()

    res = await client.post(URL, json=user_for_login)
    assert res.status == 404


async def test_user_login_incorrect_password_unauthorized(client, user_for_login: dict):
    user_for_login['password'] = random_str()

    res = await client.post(URL, json=user_for_login)
    assert res.status == 401
