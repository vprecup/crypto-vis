# create mapping for trades

```bash
curl --user elastic -X PUT "https://elastic.host.com:9200/bitfinextradesbtc" -H 'Content-Type: application/json' -d'
{
 "mappings": {
  "doc": {
   "properties": {
    "tid": {"type": "integer"},
    "price": {"type": "float"},
    "amount": {"type": "float"},
    "timestamp": {
             "type":   "date",
             "format": "epoch_millis"
            },
    "localtime":  {
             "type":   "date",
             "format": "epoch_millis"
    }
   }
  }
 }
}
'
```

# create mapping for oderbook updates

```bash
curl --user elastic -X PUT "https://elastic.host.com:9200/bitfinexbtcbookupdate" -H 'Content-Type: application/json' -d'
{
 "mappings": {
  "doc": {
   "properties": {
    "orderid": {"type": "long"},
    "price": {"type": "float"},
    "amount": {"type": "float"},
    "localtime": {
             "type":   "date",
             "format": "epoch_millis"
            }
   }
  }
 }
}
'
```

# mapping for full orderbook

```bash
curl --user elastic -X PUT "https://elastic.host.com:9200/bitfinexbtcbook" -H 'Content-Type: application/json' -d'
{
 "mappings": {
  "doc": {
   "properties": {
    "book": {
        "type": "nested"
    },
    "localtime": {
             "type":   "date",
             "format": "epoch_millis"
            }
   }
  }
 }
}
'
```