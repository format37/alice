#!/usr/bin/env python3

PORT = '8443' #prod

import asyncio
from aiohttp import web
import ssl
import firebase_admin
from firebase_admin import credentials

async def call_alice(request):
	#request_id	= request.rel_url.query['request_id']
	print("query",request.rel_url.query)
	content = "alice ok"	
	return web.Response(text=content,content_type="text/html")
	
app = web.Application()
app.router.add_route('POST', '/alice', call_alice)

ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain('fullchain.pem', 'privkey.pem')

cred = credentials.Certificate("/home/format37_gmail_com/projects/langtea/backend/json/langtea-firebase-adminsdk-q4d01-b85fc8ed07.json")
firebase_admin.initialize_app(cred)

loop = asyncio.get_event_loop()
handler = app.make_handler()
f = loop.create_server(handler, port='8081', ssl=ssl_context)
srv = loop.run_until_complete(f)

print('serving on', srv.sockets[0].getsockname())
try:
	loop.run_forever()
except KeyboardInterrupt:
	print("serving off...")
finally:
	loop.run_until_complete(handler.finish_connections(1.0))
	srv.close()