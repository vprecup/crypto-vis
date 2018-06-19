from elasticsearch import Elasticsearch
import json
import os
from dotenv import load_dotenv
import time
import requests
import logging

log = logging.getLogger(__name__)
fh = logging.FileHandler('bfx-fullbook-BTC-error.log')
fh.setLevel(logging.ERROR)
log.addHandler(fh)
logging.basicConfig(level=logging.ERROR, handlers=[fh])

load_dotenv('./.env')

es = Elasticsearch(
    [os.getenv('ELASTIC_HOST')],
    http_auth=('elastic', os.getenv('ELASTIC_PASSWORD')),
    scheme="https",
    port=9200,
)


# https://docs.bitfinex.com/v2/reference#rest-public-books
url = "https://api.bitfinex.com/v2/book/tBTCUSD/P0?len=100"
while True:
    response = None
    while response is None:
        try:
            response = requests.request("GET", url)
        except requests.exceptions.ConnectionError as e:
            print("Connection error...")
            time.sleep(5)
    try:
        book = response.json()
        orders = []
        for order in book:
            order_doc = {
                "price": order[0],
                "count": order[1],
                "amount": order[2],
            }
            orders.append(order_doc)
        doc = {
            "book": orders,
            "localtime": int(time.time()*1000)
        }
        print(doc)
        es.index(index="bitfinexbtcbook", doc_type='doc', body=json.dumps(doc))
    except Exception as e:
        print("General error caught...")
        log.error("\n%s\n%s" % (time.strftime("%d %b %Y %H:%M:%S", time.gmtime()), e))
        print("\ncrashed restarting after short nap")
        pass
    time.sleep(10) # TODO: fiddle with this