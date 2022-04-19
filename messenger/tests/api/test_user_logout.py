import pytest
from aiohttp.web import Application
from messenger.api.handlers.user_logout import UserLogoutView
from tests.user import (
    user, user_without_utc_offset, registered_user,
    user_for_login, logged_in_user, logged_in_user_headers
)
from tests.utils import get_random_str

URL = '/v1/logout'


@pytest.fixture
async def client(create_app):
    return await create_app([UserLogoutView])


async def test_user_logout_ok(client: Application, logged_in_user_headers: dict):
    res = await client.post(URL, headers=logged_in_user_headers)
    assert res.status == 201


async def test_user_logout_twice_unauthorized(client: Application, logged_in_user_headers: dict):
    res = await client.post(URL, headers=logged_in_user_headers)
    assert res.status == 201

    res = await client.post(URL, headers=logged_in_user_headers)
    assert res.status == 401


@pytest.mark.parametrize(
    'incorrect_session_id',
    [
        '',
        get_random_str(127),
        get_random_str(129),
        get_random_str(128),
    ])
async def test_user_logout_incorrect_session_id_unauthorized(
        client: Application,
        logged_in_user_headers: dict,
        incorrect_session_id: str):
    logged_in_user_headers['X-Auth-Token'] = incorrect_session_id
    res = await client.post(URL, headers=logged_in_user_headers)
    assert res.status == 401
