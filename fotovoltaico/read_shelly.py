#!/usr/bin/python3

import requests
import time
import os

url_cons = 'http://192.168.0.202/rpc/EM1Data.GetStatus?id=0' 
url_prod = 'http://192.168.0.202/rpc/EM1Data.GetStatus?id=1' 
ouput_dir='/home/paolo/solarlog/luspam.github.io/fotovoltaico/'

cons_prev = -1
prod_prev = -1

while True:
    response = requests.get(url_cons)
    if response.status_code == 200:
        data = response.json()
        cons_new = data["total_act_energy"]
    response = requests.get(url_prod)
    if response.status_code == 200:
        data = response.json()
        prod_new = data["total_act_energy"]
    ts =  time.strftime("%Y-%m-%d %H:%M:%S")
    month = time.strftime("%Y-%m")
    path = ouput_dir + month + ".csv"
    if cons_prev > 0:
        cons = round(60 * (cons_new - cons_prev))
        prod = round(60 * (prod_new - prod_prev))
        if not(os.path.isfile(path)):
            with open(path, "w") as myfile:
                myfile.write('t,consumo,produzione\n')
        with open(path, "a") as myfile:
            myfile.write('%s,%s,%s\n' % (ts, str(cons), str(prod)))
    cons_prev = cons_new
    prod_prev = prod_new
    ep = int(time.time())
    ep2 = int(ep / 60) * 60 + 90
    time.sleep(ep2 - ep)
