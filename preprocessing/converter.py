import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_json('bfxtrades.json')

# get the bid and ask data out
data = pd.DataFrame()
for k in df._source[0].keys():
    data[k]=[d[k] for d in df._source]
df = data #override it

# define the 'nachkommastellen' of the price
df['p'] = (df.price*100).astype(int)/100.0

# convert timestamp to actual time
import datetime
s=df.timestamp[0]
datetime.datetime.fromtimestamp(s/1000.0).strftime('%Y-%m-%d %H:%M:%S.%f')
df['t'] = df['timestamp'].apply(lambda x: datetime.datetime.fromtimestamp(x/1000.0).strftime('%M:%S.%f')) 

####################
# Define bin-Size
sta = int(df.price.min()*100)
sto = int(df.price.max()*100)
stepSize=0.1 #=Bin Size

priceBins = range(sta, sto, int(stepSize*100))

spec = np.zeros((len(priceBins),len(df.timestamp)))

for i, pbin in enumerate(priceBins):
    pbin/=100.0
    ix = ((df.price>=pbin) & (df.price<(pbin+stepSize)))
    spec[i,:]=np.cumsum(df.amount*ix)
    
# write out spec    



