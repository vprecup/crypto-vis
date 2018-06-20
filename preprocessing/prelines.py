import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
import json

data = None
try:
    with open('data/bfxbook.json') as f:
        data = json.loads(f.read())
        f.close()
    book = []
    prices = set()
    for step in data:
        bin = step['_source']
        sortedbin = sorted(bin['book'], key=lambda entry: entry['price'])
        orders = [{"price": item['price'],"amount": abs(item['amount'])} for item in sortedbin]
        binprices = [order['price'] for order in orders ]
        prices = prices | set(binprices)
    #print(json.dumps({
    #    'book': sorted(book, key=lambda e: e['time']),
    #}))
    ordered_prices = sorted(prices)
    #print(ordered_prices)
    #m = np.zeros(len(data),len(ordered_prices))
    m = np.zeros((len(ordered_prices),len(data)))
    print(np.shape(m))

    i = 0
    for step in data:
        bin = step['_source']
        orders = [{"price": item['price'],"amount": item['amount']} for item in bin["book"]]
        for item in orders:
            #print(item)
            #print(ordered_prices.index(item['price']))
            #m[i][ordered_prices.index(item['price'])] = item['amount']
            m[ordered_prices.index(item['price'])][i] = item['amount']
            #break
        #break
        i = i+1
    print(m)

    i = 0
    for level in m:
        print(ordered_prices[i])
        print(level)
        i = i+1
        if i == 3:
            break

except Exception as e:
    print("Error reading book data")
    print(e)









