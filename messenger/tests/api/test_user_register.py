import pytest
from aiohttp.web import Application
from messenger.api.handlers.user_register import UserRegisterView
from tests.user import user, user_without_utc_offset
from tests.utils import get_random_str

URL = '/v1/register'


@pytest.fixture
async def client(create_app):
    return await create_app([UserRegisterView])


async def test_user_register_ok(client: Application, user, user_without_utc_offset):
    res = await client.post(URL, json=user)
    assert res.status == 201

    res = await client.post(URL, json=user_without_utc_offset)
    assert res.status == 201


@pytest.mark.parametrize(
    'key,bad_value',
    [
        (k, bv)
        for k in ['login', 'password', 'user_name']
        for bv in [None, '', get_random_str(256)]
    ])
async def test_user_register_bad_params(
        client: Application,
        user,
        key: str,
        bad_value: str):
    user[key] = bad_value
    res = await client.post(URL, json=user)
    assert res.status == 400


@pytest.mark.parametrize('bad_value', [-25, 25])
async def test_user_register_bad_utc_offset(
        client: Application,
        user,
        bad_value: int):
    user['utc_offset'] = bad_value
    res = await client.post(URL, json=user)
    assert res.status == 400


async def test_user_register_twice_failed(client: Application, user):
    res = await client.post(URL, json=user)
    assert res.status == 201

    res = await client.post(URL, json=user)
    assert res.status == 400
