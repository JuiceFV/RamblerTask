from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop, make_mocked_request

from application.app import create_app
from application.settings import load_config


class AppTestCases(AioHTTPTestCase):

    async def get_application(self):
        app = await create_app(config=load_config())
        return app

    @unittest_run_loop
    async def test_index(self):
        resp = await self.client.request("GET", "/")
        assert resp.status == 200

    @unittest_run_loop
    async def test_get_token(self):
        resp = await self.client.request("GET", "/get-token")
        assert resp.status == 200
        resp = await resp.json()
        self.assertEqual(resp['token'], 'A00', msg="Received correct data")

    @unittest_run_loop
    async def test_success_post_token(self):
        resp = await self.client.request("GET", "/get-token")
        if resp.status == 200:
            resp = await self.client.request("POST", "/post-token", data={'token-field': 'A00'})
            result = await resp.json()
            self.assertEqual(result['status'], 'success')