#!/usr/bin/env python3

PORT = '8443' #prod

import asyncio
from aiohttp import web
import ssl
import firebase_admin
from firebase_admin import credentials
	
async def call_alice(request):
	
	#event = request.rel_url.query
	
	'''content = {
        'version': event['version'],
        'session': event['session'],
        'response': {
            'text': text,
            'end_session': end_session
        },
        'session_state': {'translate': translate_state, 'last_phrase': text}
    }'''
	
	#request_id	= request.rel_url.query['request_id']
	#request 			= event.get('request', {})
	#original_utterance	= request.get('original_utterance', {})
	#for item in event:
	#print( "item", request.body)
	#pprint("re",request.rel_url.query)
	
	#print('in',vars(request))
	#print('in',dir(request.rel_url.query))
	#print('in',request.rel_url.query_string)
	#print('in',request.message)
	#print('in',dir(request.rel_url))
	'''
	print('-i',len(request.rel_url.query.items()))
	print('-k',len(request.rel_url.query.keys()))
	print('-v',len(request.rel_url.query.values()))
	
	print('i',request.rel_url.query.items())
	print('k',request.rel_url.query.keys())
	print('v',request.rel_url.query.values())
	'''
	
	'''
	with open('log.txt','w') as logfile:
		logdata=''
		for v in vars(request):
			#print('---v',v)
			logdata+='\n---v '+str(v)
			for d in dir(v):
				#print('--- ---d',d)
				logdata+='\n--- ---d '+str(d)
				for c in dir(d):
					#print('--- --- ---c',c)
					logdata+='\n--- --- ---c '+str(c)
		logfile.write(logdata)
	'''
	
	data = await request.json()
	
	content = "alice ok"	
	return web.Response(text=content,content_type="text/html")

### http handle
app = web.Application()
#app.router.add_route('POST', '/alice', call_alice)
app.router.add_route('POST', '/alice', call_alice, expect_handler = web.Request.json)

### json handle
#app = web.Application()
#chooser = AcceptChooser()
#app.add_routes([web.get('/', chooser.do_route)])
#chooser.reg_acceptor('application/json', handle_json)

ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain('cert/fullchain.pem', 'cert/privkey.pem')

cred = credentials.Certificate("cert/cert.json")
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