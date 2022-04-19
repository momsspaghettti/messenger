import pytest
from aiohttp.web import Application
from messenger.api.handlers.ping import PingView
from tests.user import (
    logged_in_user, registered_user, user, user_for_login, logged_in_user_headers
)

URL = '/ping'


@pytest.fixture
async def client(create_app):
    return await create_app([PingView])


async def test_ping_with_db(client: Application):
    resp = await client.get(URL)
    assert resp.status == 200


async def test_ping_without_db(create_app):
    client = await create_app([PingView], False)

    resp = await client.get(URL)
    assert resp.status == 200


async def test_ping_with_logged_in_user(client: Application, logged_in_user_headers: dict):
    resp = await client.get(URL, headers=logged_in_user_headers)
    assert resp.status == 200
