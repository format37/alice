#!/usr/bin/env python3
import asyncio
from aiohttp import web
import urllib
import urllib.parse
from urllib.parse import urlparse, parse_qsl
import multidict as MultiDict
import requests

async def load_map(request):
	#request_id	= request.rel_url.query['request_id']
	content = "alice ok"	
	return web.Response(text=content,content_type="text/html")
	
app = web.Application()
app.router.add_route('GET', '/alice', alice)

loop = asyncio.get_event_loop()
handler = app.make_handler()
f = loop.create_server(handler, port='8081')
srv = loop.run_until_complete(f)

print('serving on', srv.sockets[0].getsockname())
try:
	loop.run_forever()
except KeyboardInterrupt:
	print("serving off...")
finally:
	loop.run_until_complete(handler.finish_connections(1.0))
	srv.close()