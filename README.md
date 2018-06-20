# Visulization of market data 

### quickstart

`python3 -m http.server` go to [http://localhost:8000/demo](http://localhost:8000/demo)

##### A D3 visualization of the dynamic evolution of the market orders for the Bitcoin crpytocurrency.

One interesting thing about a market are the trades that are offered.
This information comes in the form of the orderbook, an object consisting 
of 2 arrays the  "bids" array containg offers to buy ascendingly ordered by price
and the "asks" array containing offers to sell descendingly ordered by price.  

Each of these items contains the "amount" to be sold or bought and a "timestamp" when the offer
was put into the orderbook.

These are usually displayed as bar-graphs or opposing "valleys"


# data source

We use bitfinex as our test platform since they offer an api for the data we need and have fairly high trading volume.

## get orderbook

[rest-public-orderbook documenation](https://docs.bitfinex.com/v1/reference#rest-public-orderbook)

`curl --request GET --url https://api.bitfinex.com/v1/book/btcusd?limit_bids=100&limit_asks=100&group=1`

### example response 
```
{
  "bids": [
    {
      "price": "9082.5",
      "amount": "0.44326923",
      "timestamp": "1525219711.0"
    },
    {
      "price": "9082",
      "amount": "2.7303952",
      "timestamp": "1525219711.0"
    },
    ...
 ],
 "asks": [
    {
      "price": "9083",
      "amount": "5.34939185",
      "timestamp": "1525219711.0"
    },
    {
      "price": "9083.1",
      "amount": "1.70102282",
      "timestamp": "1525219711.0"
    },
     ...
 ]
}
```

A second interesting thing about a market is the trades actually being executed, we get these 
in the form of an array of trades descendingly  ordered by timestamp. This is usually displayed
as a line-graph over time.

## get trades

[rest-public-trades documentation](https://docs.bitfinex.com/v1/reference#rest-public-trades)

`curl --request GET   --url https://api.bitfinex.com/v1/trades/BTCUSD?limit_trades=100`


### example response

```
[
  {
    "timestamp": 1525218980,
    "tid": 237466227,
    "price": "9085.1",
    "amount": "0.01021498",
    "exchange": "bitfinex",
    "type": "buy"
  },
  ...
]
```

## Data collection + storage

Two small python programs consume these endpoints and store the results in an Elasticserch time-series database
[Getting the orderbook via REST](preprocessing/elastic_fullbook.py)
[Getting trades via Websocket](preprocessing/elastic_trades.py)
[Elastic mappings used](preprocessing/elastic-mappings.md) 

## Data processing

We use the data from Elasticsearch to generate 3 final data files to display the orderbook, the trades and the heatmap.

See the functions  `convertbook()` `converttrades()` and `convertheatmap()` in (app.py)[app.py] which also serves
as rudimentary web frontend.

## The visualization

The central graph shows price over time in as a line.
The two graphs to the right show the state of the orderbook at the selected point in time. 

The far right one shows each order separately and the middle one shows the cumulative sum of each side, which is 
the form most often used to display orderbooks (besides plain tables).

This orderbook information is also the basis for the heatmap overlaying the price graph. 
Each square shows the depth of the orderbook at that point in time at that particular price encoded using a divergent
color scale. 

This novel view of the history of orderbooks over time gives a new insight into market activities. 

## Limitations 

Obviously not being able to choose a time range, and making the resolution of the heatmap more finely grained on demand.
Also limitations in the basic data obtainable since we are always limited to 200 orders with an unknown number we can 
only see if the price gets close enough to them.