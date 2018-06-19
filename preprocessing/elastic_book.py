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
fh = logging.FileHandler('bfx-book-BTC-error.log')
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
    yield from websocket.send('{"event": "subscribe","channel": "book","pair": "BTCUSD","prec": "R0","len":"100"}')
    ack = yield from websocket.recv()
    print(" < %s " % ack)
    subscribe_ack = yield from websocket.recv()
    print(" < %s " % subscribe_ack)
    raw_snapshot = yield from websocket.recv()
    snapshot = json.loads(raw_snapshot)
    print(snapshot[1])
    # TODO: save snapshot?
    while True:
        raw = yield from websocket.recv()
        message = json.loads(raw)
        try:
            msg = message[1]
            if len(msg) == 3: # not like [17,"hb"]
                doc = {
                    "orderid": msg[0],
                    "price": msg[1],
                    "amount": msg[2],
                    "localtime": int(time.time()*1000)
                }
                print(doc)
                ret = es.index(index="bitfinexbtcbookupdate", doc_type='doc', body=json.dumps(doc))
        except KeyError as e:
            log.error("%s KEYERROR %s \n%s" % (time.strftime("%d %b %Y %H:%M:%S", time.gmtime()), raw, e))

while True:
    print("\nStarting\n")
    try:
        asyncio.get_event_loop().run_until_complete(hello())
    except Exception as e:
        log.error("\n%s\n%s" % (time.strftime("%d %b %Y %H:%M:%S", time.gmtime()), e))
        print("\ncrashed restarting after short nap\n")
        time.sleep(5)