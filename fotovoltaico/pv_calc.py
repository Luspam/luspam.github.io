#!/usr/bin/python3

import pandas as pd
from datetime import datetime, timedelta
import os

yesterday = datetime.now() - timedelta(days=1)
start = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
end = yesterday.replace(hour=23, minute=59, second=59, microsecond=999999)
month = yesterday.strftime('%Y-%m')
file_path = '/home/paolo/solarlog/luspam.github.io/fotovoltaico/{}.csv'.format(month)
df = pd.read_csv(file_path)
df.loc[:,'t'] = pd.to_datetime(df['t'])
df = df[(df['t'] >= start) & (df['t'] <= end)]
df.set_index('t', inplace=True)
df= df / 60000
df['cons_autoprodotto'] = df[['consumo', 'produzione']].min(axis=1)
df['consumo_da_rete'] = df['consumo'] - df['cons_autoprodotto']
df['prod_autoconsumata'] = df['cons_autoprodotto']
df['prod_immessa'] = df['produzione'] - df['prod_autoconsumata']
s = df.resample('D', how='sum')
s = s.round(1)
outfile = '/home/paolo/solarlog/luspam.github.io/fotovoltaico/daily/{}.csv'.format(month)
if not os.path.isfile(outfile):
    s.to_csv(outfile)
else:
    s.to_csv(outfile, mode='a', header=False)
