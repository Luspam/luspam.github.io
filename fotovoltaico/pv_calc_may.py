#!/usr/bin/python3

import pandas as pd
from datetime import datetime, timedelta

file_path = '/home/paolo/solarlog/luspam.github.io/fotovoltaico/2025-05.csv'
df = pd.read_csv(file_path)
df.loc[:,'t'] = pd.to_datetime(df['t'])

begin = datetime.now() - timedelta(days=19)
yesterday = datetime.now() - timedelta(days=1)
start = begin.replace(hour=0, minute=0, second=0, microsecond=0)
end = yesterday.replace(hour=23, minute=59, second=59, microsecond=999999)

# Filter the DataFrame for yesterday's data
df = df[(df['t'] >= start) & (df['t'] <= end)]
df.set_index('t', inplace=True)
df= df / 60000
df['cons_autoprodotto'] = df[['consumo', 'produzione']].min(axis=1)
df['consumo_da_rete'] = df['consumo'] - df['cons_autoprodotto']
df['prod_autoconsumata'] = df['cons_autoprodotto']
df['prod_immessa'] = df['produzione'] - df['prod_autoconsumata']
s = df.resample('D', how='sum')
s = s.round(1)
s.to_csv("/home/paolo/solarlog/luspam.github.io/fotovoltaico/daily/2025-05.csv")

