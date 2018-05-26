# Visulization of market data 

One interesting thing about a market are the trades that are offered.
This information comes in the form of the orderbook, an object consisting 
of 2 arrays the  "bids" array containg offers to buy ascendingly ordered by price
and the "asks" array containing offers to sell descendingly ordered by price.  

Each of these items contains the "amount" to be sold or bought and a "timestamp" when the offer
was put into the orderbook.

These are usually displayed as bar-graphs or opposing "valleys"

## get orderbook

[rest-public-orderbook documenation](https://docs.bitfinex.com/v1/reference#rest-public-orderbook)

```
    Request Details
    
    Key	Required	Type	Default	Description
    limit_bids	false	[int]	50	Limit the number of bids returned. May be 0 in which case the array of bids is empty
    limit_asks	false	[int]	50	Limit the number of asks returned. May be 0 in which case the array of asks is empty
    group	false	[0/1]	1	If 1, orders are grouped by price in the orderbook. If 0, orders are not grouped and sorted individually


    Response Detail
    
    key	Type
    bids	[array]
    price	[price]
    amount	[decimal]
    timestamp	[time]
    asks	[array]
    price	[price]
    amount	[decimal]
    timestamp	[time]
```


`curl --request GET --url https://api.bitfinex.com/v1/book/btcusd?limit_bids=100&limit_asks=100&group=1`

### example response [full](orderbook.json)
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

```
    Request Details
    
    Key	Required	Type	Default	Description
    timestamp	false	[time]		Only show trades at or after this timestamp
    limit_trades	false	[int]	50	Limit the number of trades returned. Must be >= 1
    
    Response Details

    Key	Type	Description
    tid	[integer]	
    timestamp	[time]	
    price	[price]	
    amount	[decimal]	
    exchange	[string]	"bitfinex"
    type	[string]	“sell” or “buy” (can be “” if undetermined)
```

`curl --request GET   --url https://api.bitfinex.com/v1/trades/BTCUSD?limit_trades=100`


### example response [full](trades.json)

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


## live update example

```
python test.py
INFO:btfxwss.connection:Connection opened
INFO:btfxwss.connection:API version: 2
DEBUG:btfxwss.client:_subscribe: {'symbol': 'BTCUSD', 'channel': 'ticker', 'event': 'subscribe'}
INFO:btfxwss.queue_processor:Subscription succesful for channel ('ticker', 'BTCUSD')
([[9095, 32.62270084, 9095.1, 68.38382459, -152.2, -0.0165, 9095.1, 25391.52198613, 9247.3, 8817.97469512]], 1525218355.1901114)
([[9090.9, 30.2968324, 9091, 100.52452503, -156.4, -0.0169, 9090.9, 25407.18519413, 9247.3, 8817.97469512]], 1525218372.3364313)
([[9086.6, 37.52080762, 9086.7, 112.77714807, -160.7, -0.0174, 9086.6, 25411.8386738, 9247.3, 8817.97469512]], 1525218387.138587)
([[9083.9, 33.28448941, 9084, 128.11774712, -163.3, -0.0177, 9084, 25415.31185825, 9247.3, 8817.97469512]], 1525218402.913514)
ERROR:websocket:close status: 31522
```