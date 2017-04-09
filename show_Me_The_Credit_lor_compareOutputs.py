# -*- coding: utf-8 -*-
"""
Created on Sun Apr 09 14:43:50 2017

@author: vsdak
"""

import pandas as pd
import os
import numpy as np
from sklearn import metrics

# set the path where the files are stored
path = "F:/Kaggle/honestbee_credit/"

os.chdir(path)

fls = os.listdir(path)

test1Pd = pd.read_csv("try1.csv", header = 0)

test2Pd = pd.read_csv("try1_select4best_chi.csv", header = 0)

op1 = list(test1Pd.Probability)

op2 = list(test2Pd.Probability)


print(metrics.classification_report(op1, op2))

print(metrics.confusion_matrix(op1, op2))
