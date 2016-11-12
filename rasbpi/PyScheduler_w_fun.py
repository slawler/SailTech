'''
PyScheduler.py

Notes:
1. Compatible with python v2 & v3
2. 
'''


#---Load Modules
from __future__ import print_function
import os
import glob
import time
#import matplotlib.pyplot as plt
#import pandas as pd
from datetime import datetime 
import time
import schedule
#import subprocess
#import html5lib

#---Assign directory & filename
log_dir = '/home/pi'
log_file = 'Temperature.log'
log = os.path.join(log_dir,log_file)

base_dir='/sys/bus/w1/devices/'
device_folders = glob.glob(base_dir + '28*')
print(device_folders)

#---Sensor ID's
device_table={#determined by physical check of each labelled probe
"0416807DF3FF" : "01",
"05168031B4FF" : "02",
"0516802F91FF" : "03",
"041684199FFF" : "04",
"0416841B3BFF" : "05",
"0516858720FF" : "06",
"0516858803FF" : "07",
"0416807FF4FF" : "08"}

#---Set Logging Parameters
sample_rate = 1   #seconds
logger_rate = 60  #seconds

#---Mandatory when using multiple sensors
os.system('modprobe w1-gpio') # not sure if executing these each time
time.sleep(2.0)
os.system('modprobe w1-therm')# the program is run is detrimental...
time.sleep(2.0)

#---Sensor Communication Functions 
def sort_key(address): # used by setup_read to sort the devices
    return device_table[address.upper()]

def setup_read():
    devices = []
    for d in device_folders:
        devadd = d[-12:].upper()
        print(devadd)
        if devadd in device_table:
            devices.append(devadd)
    return(sorted(devices, key=sort_key))

def read_temp_raw(device):
    filename = base_dir + '28-' + device.lower() + '/w1_slave'
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp(d):
    lines = read_temp_raw(d)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        read_temp_raw(d)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string)/1000.0
        temp_f = 32.0 + 1.8 * temp_c
        return temp_c, temp_f

devices = setup_read()

print("  # address\n---------------")
for d in devices:
    print(" " + device_table[d.upper()] + " " + d)
print(" ",end="")

for d in devices:
    print('{:s}'.format(" " + device_table[d.upper()]+ " |"),end="")
print("\n"+len(devices)*"-----")


#---Delete all scheduled jobs
schedule.clear()

#---Sampling funciton: Record data to log  
def job1():
    dtm  = datetime.now().strftime(format = '%d.%Y.%m %H:%M:%S')
    with open(log,'a') as f:
        for d in devices:
            temps = read_temp(d)
            print('{:4.1f}|'.format(temps[0]),end="")
            d_id = str(device_table[d.upper()])
            f.write(dtm + '\t' +d_id + '\t'+ '{}'.format(temps[0])+ '\n')   

    #print("Time: {0}, Temperature (F): {1}".format(dtm, temps))

#---Logging funciton: Create Plot, Push updates to remote    
def job2():
    print("Update Log")
    return('') 

#---Initialize Scheduler to call jobs
schedule.every(sample_rate).seconds.do(job1)
schedule.every(logger_rate).seconds.do(job2)

#---Run Jobs
while True:
    try:
        schedule.run_pending()
        time.sleep(1)
        print(" ",end="\r")

        
    except KeyboardInterrupt:
        print('Process Terminated')
        break
    
'''
#--Read in Data from most recent log
cols = ['time','Forward','Main','Aft','Outside']
df = pd.read_csv(log, sep = '\t', header = None, names = cols)
df = df.set_index(pd.to_datetime(df['time'],format = '%d.%Y.%m %H:%M:%S'))
df.drop(labels='time',axis=1, inplace= True)
#df.head()

#---PLot data from most recent log
df.plot(x = df.index, y = ['Forward','Main','Aft','Outside'])
plt.title('Pegasus Temperature Log'+ '\n Begining {}'.format(df.index[0]))
plt.ylabel('Temperature (F)')
plt.xlabel('Time')
plt.grid(True)
plt.ylim((20,75))

#---Read most recent log saved on github, look at last few entries

cols = ['time','Forward','Main','Aft','Outside']
url = 'https://raw.githubusercontent.com/slawler/DataAnalytics/master/SailTech/logs/Temperature.log'

gitlog = pd.read_csv(url, sep = '\t', header = None, names = cols)
gitlog = gitlog.set_index(pd.to_datetime(gitlog['time'],format = '%d.%Y.%m %H:%M:%S'))
gitlog.drop(labels='time',axis=1, inplace= True)
gitlog.tail()
'''
