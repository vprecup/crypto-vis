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
fh = logging.FileHandler('kraken-trades-USDT-error.log')
fh.setLevel(logging.DEBUG)
log.addHandler(fh)
logging.basicConfig(level=logging.DEBUG, handlers=[fh])

since = ""
while True:
    try:
        url = "https://api.kraken.com/0/public/Trades?pair=USDTUSD&since=" + since
        response = requests.request("GET", url)
        data = response.json()
        if len(data["error"]) == 0:
            trades = data["result"]["USDTZUSD"]
            for trade in trades:
                doc = {
                    "price": trade[0],
                    "volume": trade[1],
                    "timestamp": int((trade[2])*1000),
                    "side": trade[3],
                    "type": trade[4],
                    "misc": trade[5],
                    "localtime": int(time.time()*1000)
                }
                print(doc)
                es.index(index="krakentradesusdt", doc_type='doc', body=json.dumps(doc))
            since = data["result"]["last"]
        else:
            log.error("%s" % data)
    except Exception as e:
        log.error("%s - %s" % (e, data))
    time.sleep(5)

""" ELASTIC index:
curl --user elastic -X PUT "https://elastic.host.com:9200/krakentradesusdt" -H 'Content-Type: application/json' -d'
{
 "mappings": {
  "doc": {
   "properties": {
       "price": {"type": "double"},
       "volume": {"type": "double"},
       "timestamp":  {
                "type":   "date",
                "format": "epoch_millis"
       },
       "side": {"type": "text"},
       "type": {"type": "text"},
       "misc": {"type": "text"},
       "localtime":  {
                "type":   "date",
                "format": "epoch_millis"
       }
   }
  }
 }
}
'
"""