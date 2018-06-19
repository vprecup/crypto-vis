import pandas as pd
import matplotlib.pyplot as plt
import datetime

#### Bucket-Size Definition ##############
# Price Bucket-size
stepSize = 3 #define Step-Size of Bins
# Time Bucket-size
tFreq = 'min' #frequency of time-Buckets

########## Load Data
df = pd.read_json('data/bfxbook.json') # has all the trades
#df = pd.read_json('bfxtrades.json')

#### get right format
data = pd.DataFrame(df._source[0]['book'])
time = df._source[0]['localtime']
data['localtime'] = time
data['t'] = datetime.datetime.fromtimestamp(time/1000.0).strftime('%M:%S.%f')
all_data = pd.DataFrame()

for i in range(len(df)):
    data = pd.DataFrame(df._source[i]['book'])
    time = df._source[i]['localtime']
    data['localtime'] = time
    data['t'] = datetime.datetime.fromtimestamp(time/1000.0).strftime('%Y-%m-%d %H:%M')#%Y-%m-%d #:%S.%f
    all_data = pd.concat([data,all_data], axis=0)
df = all_data

# sort it
df = df.sort_values('localtime')

timerange = pd.date_range(start=min(df.t), end=max(df.t), freq=tFreq).strftime('%Y-%m-%d %H:%M').tolist()

priceBins = np.arange(df.price.min(),df.price.max(),stepSize)

volumeArray = np.zeros((len(priceBins),len(set(timerange))))


outData=[]
for i, pbin in enumerate(priceBins[1:]):
    ix = ((df.price>=priceBins[i]) & (df.price<(priceBins[i+1])))
    for it, t in enumerate(timerange):
        vol = sum(df[(df.t==t)&ix].amount)
        volumeArray[i,it]= vol
        if vol>1:
            outData.append([t, pbin, vol]) 
            
out = pd.DataFrame(outData,columns=['x','y','vol'])
out.to_csv('volArray.csv',index=False)