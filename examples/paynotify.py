#!/usr/bin/env python
import asyncio
import websockets
import redis
import hashlib
import logging
from daemon3 import Daemon

async def response(websocket, path):
    global ris
    order_id = await websocket.recv()
    mdf = hashlib.md5()
    mdf.update(order_id.encode(encoding='utf-8'))
    key = mdf.hexdigest()
    logging.info("recv message order id is: %s => %s " % (order_id, key))
    while True:
        await asyncio.sleep(2)
        msg = 'ID' + ' : ' + key
        val = ris.get(key)
        if val != None:
            await websocket.send(order_id)
            ris.delete(key)
            break

def main():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='/tmp/websocket.log',
                        filemode='w')
    start_server = websockets.serve(response, '0.0.0.0', 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

class WebSocketServer(Daemon):
    def run(self):
        main()

if "__main__" == __name__:
    ris = redis.Redis(host='2324083c6acc46c9.m.cnsza.kvstore.aliyuncs.com', port=6379, db=0, password='root:RMTHpts80808com')
    ws = WebSocketServer('/tmp/websocketserver.pid')
    ws.start()
    #main();