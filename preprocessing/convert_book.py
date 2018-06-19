import datetime
import json

data = None
try:
    with open('bfxbook.json') as f:
        data = json.loads(f.read())
        f.close()
    book = []
    minprice = 10000000.0   # adjust according to mooning
    maxprice = 0.0
    maxtotal = 0.0
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

        bids = [{"price": item['price'],"amount": abs(item['amount'])} for item in sortedbin if item['amount'] > 0]
        bidTotal = 0.0
        if bids[-1]['price'] < minprice:
            minprice = bids[-1]['price']
        for i in range(len(bids)):
            bidTotal = bidTotal + bids[i]['amount']
            bids[i]['total'] = bidTotal
            if bidTotal > maxtotal:
                maxtotal = bidTotal

        datum = {
            'time': bin['localtime'],
            'asks': sorted(asks, key=lambda e: e['price'], reverse=True),
            'bids': sorted(bids, key=lambda e: e['price'], reverse=True)
        }
        book.append(datum)
    print(json.dumps({
            'extent': [minprice, maxprice],
            'book': sorted(book, key=lambda e: e['time']),
            'maxtotal': maxtotal
    }))
except:
    print("Error reading book data")








