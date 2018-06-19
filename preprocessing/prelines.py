import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
import json

data = None
try:
    with open('../bfxbook.json') as f:
        data = json.loads(f.read())
        f.close()
    book = []
    prices = set()
    for step in data:
        bin = step['_source']
        sortedbin = sorted(bin['book'], key=lambda entry: entry['price'], reverse=True)
        orders = [{"price": item['price'],"amount": abs(item['amount'])} for item in sortedbin]
        #print(sortedbin)
        datum = {
            'time': bin['localtime'],
            'orders':sorted(orders, key=lambda e: e['price'], reverse=True)
        }
        binprices = [order['price'] for order in orders ]
       # print(set(binprices))
        prices = prices | set(binprices)
        book.append(datum)
        #for item in orders:
        #    print(item['price'])
        #    print(set(item['price']))
    #print(json.dumps({
    #    'book': sorted(book, key=lambda e: e['time']),
    #}))
    ordered_prices = sorted(prices)
    print(ordered_prices)
except:
    print("Error reading book data")









