# Kraken public market data api

## recent trades 

https://api.kraken.com/0/public/Trades?pair=USDTUSD
>
    Get recent trades
    URL: https://api.kraken.com/0/public/Trades
    
    Input:
    
    pair = asset pair to get trade data for
    since = return trade data since given id (optional.  exclusive)
    Result: array of pair name and recent trade data
    
    <pair_name> = pair name
        array of array entries(<price>, <volume>, <time>, <buy/sell>, <market/limit>, <miscellaneous>)
    last = id to be used as since when polling for new trade data
    
    
```json
{
    "error": [],
    "result": {
        "USDTZUSD": [
            [
                "0.99790000",
                "20.69704832",
                1527025571.322,
                "b",
                "l",
                ""
            ]
        ],
        "last": "1527101374051100324
    }
}
```

https://api.kraken.com/0/public/Trades?pair=USDTUSD&since=1527101671792450451
```json
{
    "error": [],
    "result": {
        "USDTZUSD": [],
        "last": "1527101671792450451"
    }
}
```

## order book

>
    Get order book
    URL: https://api.kraken.com/0/public/Depth
    
    Input:
    
    pair = asset pair to get market depth for
    count = maximum number of asks/bids (optional)
    Result: array of pair name and market depth
    
    <pair_name> = pair name
        asks = ask side array of array entries(<price>, <volume>, <timestamp>)
        bids = bid side array of array entries(<price>, <volume>, <timestamp>)