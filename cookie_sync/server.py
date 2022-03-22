import time
from aiohttp import web
from typing import Dict, List, Union
import aiohttp
import json
import threading
import asyncio


def _run_server(
        session: aiohttp.ClientSession,
        cookie_names: List[str],
        domain: str,
):
    async def websocket_handler(request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        await ws.send_json({
            'action': 'get',
            'cookies': cookie_names,
            'domain': domain,
        })

        async for msg in ws:
            if msg.type != aiohttp.WSMsgType.TEXT:
                continue

            try:
                msg_json: Union[List, Dict] = msg.json()

                cookies: List[Dict[str, str]] = msg_json \
                    if isinstance(msg_json, list) else [cookies]

            except json.decoder.JSONDecodeError:
                continue

            for c in cookies:
                session.cookie_jar.update_cookies(c)

        return ws

    app = web.Application()
    app.add_routes([web.get('/ws', websocket_handler)])

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    web.run_app(app, host='localhost', port=3001)


def run_server(
        session: aiohttp.ClientSession,
        domain: str,
        cookies: List[str] = [],
        wait_for_cookies: bool = True,
        timeout: int = 30,
):
    threading.Thread(
        target=_run_server,
        args=(session, cookies, domain,),
        daemon=True
    ).start()

    if wait_for_cookies:
        t = time.time()

        while not len(session.cookie_jar):
            if (time.time() - t) > timeout:
                break

            pass
