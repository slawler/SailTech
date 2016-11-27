# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#Import Libraries
#Download tar.gz from https://github.com/slawler/PegasusLogs/tree/master/signalk

import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

sample_data = "log.txt"
df = pd.read_csv(sample_data, header = None, sep = '\t')
df = df.pivot(index = 0, columns=1, values=2)
df = df.set_index(pd.to_datetime(df.index,format = '%Y-%m-%d %H:%M:%S'))
df = df.resample('5S').mean()
df.index.name = None
df.columns.name = None
df.to_hdf('log.h5','df',mode='w',format='table',data_columns=True)
 
df.to_csv('log.csv',sep=',')
#plt.scatter(x=df.index,y=df.windspeedApparent)