import pytest
from .utils import random_str, utc_offset
from messenger.api.handlers.user_register import UserRegisterView
from messenger.api.handlers.user_login import UserLoginView


@pytest.fixture
def logged_in_user_headers(logged_in_user: str):
    return {'X-Auth-Token': logged_in_user}


@pytest.fixture
async def logged_in_user(user_for_login: dict, create_app):
    url = '/v1/login'

    client = await create_app([UserLoginView])

    res = await client.post(url, json=user_for_login)

    assert res.status == 201

    res_json = await res.json()
    assert 'session_id' in res_json
    session_id = res_json['session_id']
    assert isinstance(session_id, str)
    assert len(session_id) == 128

    return session_id


@pytest.fixture
def user_for_login(registered_user: dict) -> dict:
    return {
        'login': registered_user['login'],
        'password': registered_user['password']
    }


@pytest.fixture
async def registered_user(user, create_app):
    url = '/v1/register'

    client = await create_app([UserRegisterView])

    res = await client.post(url, json=user)
    assert res.status == 201

    return user


@pytest.fixture
def user():
    return get_user(True)


@pytest.fixture
def user_without_utc_offset():
    return get_user()


def get_user(with_utc_offset: bool = False) -> dict:
    user = {
        'login': random_str(),
        'password': random_str(),
        'user_name': random_str()
    }

    if with_utc_offset:
        user['utc_offset'] = utc_offset()

    return user
