import time
import os

devs = ['/sys/bus/w1/devices/28-3c840457ce28/w1_slave', '/sys/bus/w1/devices/28-3ce1d443e517/w1_slave']
ouput_dir='/home/paolo/solarlog/luspam.github.io/riscaldamento/'

t = ["", ""]
for i in range(0, 2):
    with open(devs[i]) as f:
        lines = f.readlines()
        if len(lines) == 2 and "YES" in lines[0]:
            k = lines[1].find("t=")
            if k > 0:
                t[i] = str(round(float(lines[1][k+2:].replace("\n", "")) / 1000, 1))

with open('/sys/class/gpio/gpio9/value', 'r') as file:
    p0 = 15 + 25 * int(file.readline().strip())
with open('/sys/class/gpio/gpio8/value', 'r') as file:
    p1 = 15 + 25 * int(file.readline().strip())
ts =  time.strftime("%Y-%m-%d %H:%M:%S")
month = time.strftime("%Y-%m")
path = ouput_dir + month + ".csv"
if not(os.path.isfile(path)):
    with open(path, "w") as myfile:
        myfile.write('t,T0,T1,P0,P1\n')
with open(path, "a") as myfile:
    myfile.write('%s,%s,%s,%d,%d\n' % (ts, t[0], t[1], p0, p1))

