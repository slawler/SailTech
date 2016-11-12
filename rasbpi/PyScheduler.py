In [ ]:
#---Load Modules
% matplotlib notebook
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime 
import time
import schedule
import os
import subprocess
import html5lib
import random #--For testing only, remove for implementation
In [ ]:
#---Assign directory & filename
log_dir = '/home/slawler'
log_file = 'Temperature.log'
log = os.path.join(log_dir,log_file)

#---Set Parameters
sample_rate = 1 #seconds
logger_rate = 60  #seconds
  
#---Delete all scheduled jobs
schedule.clear()

#---Placeholder for Sampling funciton. 
def job1():
    dtm  = datetime.now().strftime(format = '%d.%Y.%m %H:%M:%S')
    
    t1 = round(random.uniform(55,60),2)
    t2 = round(random.uniform(50,55),2)
    t3 = round(random.uniform(53,57),2)
    t4 = round(random.uniform(25,30),2)
    temps = str(t1)+'\t'+str(t2)+'\t'+str(t3)+'\t'+str(t4)
                                          
    with open(log,'a') as f: 
        f.write(dtm + '\t' + temps + '\n')   
    
    print("Time: {0}, Temperature (F): {1}".format(dtm, temps))

#---Placeholder for Logging funciton.    
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
    except KeyboardInterrupt:
        print('Process Terminated')
        break
In [ ]:
#--Read in Data from most recent log

cols = ['time','Forward','Main','Aft','Outside']
df = pd.read_csv(log, sep = '\t', header = None, names = cols)
df = df.set_index(pd.to_datetime(df['time'],format = '%d.%Y.%m %H:%M:%S'))
df.drop(labels='time',axis=1, inplace= True)
df.head()
In [ ]:
#---PLot data from most recent log
df.plot(x = df.index, y = ['Forward','Main','Aft','Outside'])
plt.title('Pegasus Temperature Log'+ '\n Begining {}'.format(df.index[0]))
plt.ylabel('Temperature (F)')
plt.xlabel('Time')
plt.grid(True)
plt.ylim((20,75))
In [ ]:
#---Read most recent log saved on github, look at last few entries

cols = ['time','Forward','Main','Aft','Outside']
url = 'https://raw.githubusercontent.com/slawler/DataAnalytics/master/SailTech/logs/Temperature.log'

gitlog = pd.read_csv(url, sep = '\t', header = None, names = cols)
gitlog = gitlog.set_index(pd.to_datetime(gitlog['time'],format = '%d.%Y.%m %H:%M:%S'))
gitlog.drop(labels='time',axis=1, inplace= True)
gitlog.tail()
