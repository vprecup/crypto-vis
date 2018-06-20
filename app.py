from flask import Flask
from elasticsearch import Elasticsearch
import os
import json
from dotenv import load_dotenv
from operator import itemgetter
import numpy as np
import pandas as pd
import datetime
import time as ttime

load_dotenv('./.env')


def dumpindex(es, index, body, filename):
    print("Dumping %s" % index)
    # this is a bit complicated first we need to get size then request them all explicitly
    count_result = es.search(index=index, body=json.dumps(body))
    count = int(count_result["hits"]["total"])
    print("Found %s hits" % count)
    # now actually get them all
    result = es.search(index=index, body=json.dumps(body),size=count)
    tradefile = open(filename, "w")
    tradefile.write(json.dumps(result["hits"]["hits"]))
    tradefile.close()


def elasticget():
    es = Elasticsearch(
        [os.getenv('ELASTIC_HOST')],
        http_auth=('elastic', os.getenv('ELASTIC_PASSWORD')),
        scheme="https",
        port=9200,
    )
    body = {
        "query": {
            "range": {
                "timestamp": {
                    "gte": "now-1h",
                    "lte": "now"
                }
            }
        }
    }

    dumpindex(es, "bitfinextradesbtc", body, "static/bfxtrades.json")

    # book and updates indexed by "localtime"
    body = {
        "query": {
            "range": {
                "localtime": {
                    "gte": "now-1h",
                    "lte": "now"
                }
            }
        }
    }

    dumpindex(es, "bitfinexbtcbook", body, "static/bfxbook.json")

def convertbook():
    data = None
    try:
        with open('static/bfxbook.json') as f:
            data = json.loads(f.read())
            f.close()
        book = []
        minprice = 10000000.0   # adjust according to mooning
        maxprice = 0.0
        maxtotal = 0.0
        maxvolume = 0.0
        for step in data:
            bin = step['_source']
            sortedbin = sorted(bin['book'], key=lambda entry: entry['price'], reverse=True)

            asks = [{"price": item['price'],"amount": abs(item['amount'])} for item in sortedbin if item['amount'] < 0]
            askTotal = 0.0
            if asks[0]['price'] > maxprice:
                maxprice = asks[0]['price']
            for i in range(len(asks)-1, -1, -1):
                askTotal = askTotal + asks[i]['amount']
                asks[i]['total'] = askTotal
                if askTotal > maxtotal:
                    maxtotal = askTotal
                if asks[i]['amount'] > maxvolume:
                    maxvolume = asks[i]['amount']

            bids = [{"price": item['price'],"amount": abs(item['amount'])} for item in sortedbin if item['amount'] > 0]
            bidTotal = 0.0
            if bids[-1]['price'] < minprice:
                minprice = bids[-1]['price']
            for i in range(len(bids)):
                bidTotal = bidTotal + bids[i]['amount']
                bids[i]['total'] = bidTotal
                if bidTotal > maxtotal:
                    maxtotal = bidTotal
                if bids[i]['amount'] > maxvolume:
                    maxvolume = bids[i]['amount']

            datum = {
                'time': bin['localtime'],
                'asks': sorted(asks, key=lambda e: e['price'], reverse=True),
                'bids': sorted(bids, key=lambda e: e['price'], reverse=True)
            }
            book.append(datum)
        out = json.dumps({
            'extent': [minprice, maxprice],
            'book': sorted(book, key=lambda e: e['time']),
            'maxtotal': maxtotal,
            'maxvolume': maxvolume
        })
        with open('static/processed_book.json',"w") as o:
            o.write(out)
            o.close()
    except Exception as e:
        print("Error reading book data")
        print(e)

def converttrades():
    with open("static/bfxtrades.json","r") as datafile:
        data = json.loads(datafile.read())
        ndata = []
        for dat in data:
            ndata.append(dat["_source"])

        newlist = sorted(ndata, key=itemgetter('timestamp'), reverse=False)

        datafile.close()
        with open("static/trades.tsv", "w") as out:
            out.write("date\tprice\tamount\n")
            for dat in newlist:
                out.write("%s\t%s\t%s\n" % (dat["timestamp"], dat["price"], dat["amount"]))
            out.close()

# time conversion stuff
def datetime_to_epoch_ms(datetime_string):
    dt = datetime.datetime.strptime(datetime_string, '%Y-%m-%d %H:%M')
    return int(ttime.mktime(dt.timetuple()) * 1000)


def convertheatmap():
    #### Bucket-Size Definition ##############
    # Price Bucket-size
    stepSize = 3 #define Step-Size of Bins
    # Time Bucket-size
    tFreq = 'min' #frequency of time-Buckets

    ########## Load Data
    df = pd.read_json('static/bfxbook.json') # has all the trades
    #df = pd.read_json('bfxtrades.json')

    #### get right format
    data = pd.DataFrame(df._source[0]['book'])
    time = df._source[0]['localtime']
    data['localtime'] = time
    data['t'] = datetime.datetime.fromtimestamp(time/1000.0).strftime('%M:%S.%f')
    all_data = pd.DataFrame()

    for i in range(len(df)):
        data = pd.DataFrame(df._source[i]['book'])
        time = df._source[i]['localtime']
        data['localtime'] = time
        data['t'] = datetime.datetime.fromtimestamp(time/1000.0).strftime('%Y-%m-%d %H:%M')#%Y-%m-%d #:%S.%f
        all_data = pd.concat([data,all_data], axis=0)
    df = all_data

    # sort it
    df = df.sort_values('localtime')

    timerange = pd.date_range(start=min(df.t), end=max(df.t), freq=tFreq).strftime('%Y-%m-%d %H:%M').tolist()

    priceBins = np.arange(df.price.min(),df.price.max(),stepSize)

    volumeArray = np.zeros((len(priceBins),len(set(timerange))))


    outData=[]
    for i, pbin in enumerate(priceBins[1:]):
        ix = ((df.price>=priceBins[i]) & (df.price<(priceBins[i+1])))
        for it, t in enumerate(timerange):
            vol = sum(df[(df.t==t)&ix].amount)
            volumeArray[i,it]= vol
            if vol>0.1 or vol<-0.1:
                outData.append([datetime_to_epoch_ms(t), pbin, (vol)])

    out = pd.DataFrame(outData,columns=['date','price','vol'])
    out.to_csv('static/volArray.csv',index=False)

from flask import render_template

app = Flask(__name__)
@app.route("/")
def index():
    print("Get data")
    elasticget()
    print("Convert book")
    convertbook()
    print("Convert trades")
    converttrades()
    print("Generate heatmap")
    convertheatmap()
    return render_template('index.html')


@app.route('/stat')
def stat(name=None):
    return render_template('index.html')

@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

"""
cp .env.dist .env
# and fill out .env file
"""

if __name__ == '__main__':
    print("Get data")
    elasticget()
    print("Convert book")
    convertbook()
    print("Convert trades")
    converttrades()
    print("Generate heatmap")
    convertheatmap()

