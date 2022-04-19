from messenger.api.handlers.ping_db import PingDbView


async def test_ping_with_db(create_app):
    url = '/ping_db'

    client = await create_app([PingDbView], True)

    resp = await client.get(url)
    assert resp.status == 200


async def test_ping_without_db(create_app):
    url = '/ping_db'

    client = await create_app([PingDbView], False)

    resp = await client.get(url)
    assert resp.status == 503
