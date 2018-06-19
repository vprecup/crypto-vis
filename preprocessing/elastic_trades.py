from elasticsearch import Elasticsearch
import asyncio
import websockets
import json
import os
from dotenv import load_dotenv
import certifi
import time
import logging
load_dotenv('./.env')

log = logging.getLogger(__name__)
fh = logging.FileHandler('bfx-trades-BTC-error.log')
fh.setLevel(logging.ERROR)
log.addHandler(fh)
logging.basicConfig(level=logging.ERROR, handlers=[fh])

@asyncio.coroutine
def hello():
    es = Elasticsearch(
        [os.getenv('ELASTIC_HOST')],
        http_auth=('elastic', os.getenv('ELASTIC_PASSWORD')),
        scheme="https",
        port=9200,
    )

    websocket = yield from websockets.connect('wss://api.bitfinex.com/ws/2')
    yield from websocket.send('{"event":"subscribe","channel":"trades","symbol":"BTCUSD"}')
    ack = yield from websocket.recv()
    #    print(ack)
    lasttrades = yield from websocket.recv()
    #    print(lasttrades)
    while True:
        raw = yield from websocket.recv()
        message = json.loads(raw)
        try:
            if message[1] == "tu":
                msg = message[2]
                print(msg)
                doc = {
                    "tid": msg[0],
                    "timestamp": msg[1],
                    "amount": msg[2],
                    "price": msg[3],
                    "localtime": int(time.time()*1000)
                }
                es.index(index="bitfinextradesbtc", doc_type='doc', body=json.dumps(doc))
        except KeyError as e:
            log.error("%s KEYERROR %s \n%s" % (time.strftime("%d %b %Y %H:%M:%S", time.gmtime()), raw, e))

asyncio.get_event_loop().run_until_complete(hello())

while True:
    print("\nStarting\n")
    try:
        asyncio.get_event_loop().run_until_complete(hello())
    except Exception as e:
        log.error("\n%s\n%s" % (time.strftime("%d %b %Y %H:%M:%S", time.gmtime()), e))
        print("\ncrashed restarting after short nap")
        time.sleep(1)