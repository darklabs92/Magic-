# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 22:21:04 2017

@author: vsdak
"""

import os
import pandas as pd
import numpy as np

# set the working directory
#path = "D:/training/randomProg/c2r/"
path = "F:/datasets/lazada_data/key_value/"
os.chdir(path)
fls3=os.listdir(path)


for a2 in fls3:
    if a2[-4:]=='.csv':
        structDf = pd.read_csv(a2, header=0)

structDf.columns
key = list(structDf.key)
value = list(structDf.value)

distKey = list(np.unique(key))
distVal = [0 for m in distKey]

for j in range(len(key)):
    for i in range(len(distKey)):
        if key[j]==distKey[i]:
            distVal[i] = distVal[i]+value[j]
            break
            
