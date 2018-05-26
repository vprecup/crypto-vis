import requests
import time
import logging
import json
import os
from elasticsearch import Elasticsearch
from dotenv import load_dotenv

load_dotenv('../.env')

es = Elasticsearch(
    [os.getenv('ELASTIC_HOST')],
    http_auth=('elastic', os.getenv('ELASTIC_PASSWORD')),
    scheme="https",
    port=9200,
)

log = logging.getLogger(__name__)
fh = logging.FileHandler('kraken-book-USDT-error.log')
fh.setLevel(logging.DEBUG)
log.addHandler(fh)
logging.basicConfig(level=logging.DEBUG, handlers=[fh])

while True:
    try:
        url = "https://api.kraken.com/0/public/Depth?pair=USDTZUSD&count=200"
        response = requests.request("GET", url)
        data = response.json()
        if len(data["error"]) == 0:
            book = data["result"]["USDTZUSD"]
            asks = book["asks"]
            bids = book["bids"]
            ask_doc = []
            for ask in asks:
                ask_doc.append({
                    "price": ask[0],
                    "volume": ask[1],
                    "timestamp": ask[2]
                })
            bid_doc = []
            for bid in bids:
                bid_doc.append({
                    "price": bid[0],
                    "volume": bid[1],
                    "timestamp": bid[2]
                })
            doc = {
                "asks": ask_doc,
                "bids": bid_doc,
                "timestamp": int(time.time()*1000)
            }
            print("%s %s " % (asks[0][:2], bids[0][:2]))
            es.index(index="krakenbookusdt", doc_type='doc', body=json.dumps(doc))
        else:
            log.error("%s" % data)
    except Exception as e:
        log.error("%s - %s" % (e, data))
    time.sleep(10)


""" ELASTIC index:
curl --user elastic -X PUT "https://elastic.host.com:9200/krakenbookusdt" -H 'Content-Type: application/json' -d'
{
 "mappings": {
  "doc": {
   "properties": {
       "asks": {
        "type": "nested"
        },
        "bids": {
        "type": "nested"
        },
       "timestamp":  {
                "type":   "date",
                "format": "epoch_millis"
       }
   }
  }
 }
}
'
"""