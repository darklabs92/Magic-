# -*- coding: utf-8 -*-
"""
Created on Thu Apr 06 00:47:58 2017

@author: vsdaking
"""

###
# Intial Environment setup and reading of files
###

# Aim of program is to predict peopl most likely to default on their payment,
# based on their past credit usage patterns

# import the necessary packages
import pandas as pd
import numpy as np
import math
import os
import copy
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')
from pandas.tools.plotting import scatter_matrix

# set the path where the files are stored
path = "F:/Kaggle/honestbee_credit/"

os.chdir(path)

fls = os.listdir(path)

# read in the train DS (data set) specifically
trainPd = pd.read_csv(path+"cs-training.csv", header=0)

trainPd.columns

# observed that the names did not change despite changes made in the CSV
# hence, change the names explicitly below
cols = ['id','seriousDlq2yr','revolvngUnsecuredUtilised','age',
                   'num30to59only','debtRatio','monthlyIncm','numOpenCrdNLoan',
                   'num90aab','numFixedLines','num60to89only','fmlyMembrs']

trainPd.columns = cols

###
# Initial data exploration and data sanity checks 
###

# determine how many NULL values exist across DS
colNullCnt = []

for z in range(len(cols)):
    colNullCnt.append([cols[z], sum(pd.isnull(trainPd[cols[z]]))])

colNullCnt

# view how each variable is distributed and come up with initial prognosis
for z2 in range(len(cols)):
    print cols[z2]
    trainPd[cols[z2]].plot.box()
    fig = plt.figure()
    trainPd[cols[z2]].plot.hist()
    plt.show()
    #trainPd.plot.scatter(y='seriousDlq2yr', x=cols[z2])
    print ""
    print ""
    
# we hereby learn that possibly one of the most critical variables - monthly income - almost has 
# a staggering 20% values as missing / NaN!
# this leads me to question how much more dirty is this data ..?
# depending on each scenario, we can determine how to proceed - 
#   1. impute the values via simple stats (mean, median, mode, etc.)
#   2. predict the values based on other factors
#   3. discard the record altogether, as this brings in questions of data integrity (how do we know how valid / correct is the rest of that given entry?!)
#   4. use a filler / predetermined value in place of the missing values
# given the huge no of missing vals, we can rule out option 3 as it will greatly decrease our # of training records
# also, since monthly income may lead to be an impactful variable, it may not be in our best interests to use a fixed Monthly Income for the widely varying range of data points (records) we have
# so, for now, let us use a simple mean of 

scatter_matrix(trainPd, alpha=0.5, figsize=(12, 12), diagonal='kde')

