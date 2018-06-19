import json
import datetime
from operator import itemgetter


converted = []
with open("../bfxtrades.json","r") as datafile:
    data = json.loads(datafile.read())
    ndata = []
    for dat in data:
        ndata.append(dat["_source"])

    newlist = sorted(ndata, key=itemgetter('timestamp'), reverse=False)

    datafile.close()
    with open("trades.tsv", "w") as out:
        out.write("date\tprice\tamount\n")
        for dat in newlist:
            out.write("%s\t%s\t%s\n" % (dat["timestamp"], dat["price"], dat["amount"]))
        out.close()