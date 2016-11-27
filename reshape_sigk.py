# -*- coding: utf-8 -*-
"""
Description:Reshape raw data from signal k stream to pandas dataframe
@author: slawler@dewberry.com
Created on Sun Nov 27 10:34:36 2016
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
