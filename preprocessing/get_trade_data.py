"""
cp .env.dist .env
# and fill out .env file
"""
from elasticsearch import Elasticsearch
import os
import json
from dotenv import load_dotenv
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


if __name__ == "__main__":
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
                    "lt": "now"
                }
            }
        }
    }

    dumpindex(es, "bitfinextradesbtc", body, "bfxtrades.json")

    # book and updates indexed by "localtime"
    body = {
        "query": {
            "range": {
                "localtime": {
                    "gte": "now-1h",
                    "lt": "now"
                }
            }
        }
    }

    dumpindex(es, "bitfinexbtcbook", body, "bfxbook.json")
    # still gotta work on dumping updates they are too large...
    # elasticsearch.exceptions.TransportError: TransportError(500, 'search_phase_execution_exception', 'Result window is too large, from + size must be less than or equal to: [10000] but was [133801]. See the scroll api for a more efficient way to request large data sets. This limit can be set by changing the [index.max_result_window] index level setting.')
    # dumpindex(es, "bitfinexbtcbookupdate", body, "bfxbookupdate.json")
