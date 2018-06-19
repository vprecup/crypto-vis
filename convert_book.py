import datetime
import json

data = None
try:
    with open('bfxbook.json') as f:
        data = json.loads(f.read())
        f.close()
except:
    print("Error reading book data")

bin = data[0]['_source']
sortedbin = sorted(bin['book'], key=lambda entry: entry['price'], reverse=True)

asks = [{"price": item['price'],"amount": abs(item['amount'])} for item in sortedbin if item['amount'] < 0]
askTotal = 0.0
for i in range(len(asks)-1, -1, -1):
    askTotal = askTotal + asks[i]['amount']
    asks[i]['total'] = askTotal

bids = [{"price": item['price'],"amount": abs(item['amount'])} for item in sortedbin if item['amount'] > 0]
bidTotal = 0.0
for i in range(len(bids)):
    bidTotal = bidTotal + bids[i]['amount']
    bids[i]['total'] = bidTotal

datum = {
    'time': bin['localtime'],
    'asks': sorted(asks, key=lambda e: e['price'], reverse=True),
    'bids': sorted(bids, key=lambda e: e['price'], reverse=True)
}

print(json.dumps(datum))






