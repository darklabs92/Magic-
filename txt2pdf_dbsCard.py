# -*- coding: utf-8 -*-
"""
Created on Tue Nov 01 23:32:37 2016

@author: vsdak
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Nov 01 22:47:32 2016

@author: vsdak
"""

import os
import pandas as pd
import numpy as np

# set the working directory
path = "F:/banking/payments/"
os.chdir(path)
fils2 = os.listdir(path)

for f in fils2:
    if f[-4:]==".txt":
        # Method 1 to read txt file
        with open(f, 'r') as file:
            fileList = file.readlines()
        otp = [['Date','Description','Amount'] for i in range(1)]
        metadata = [[str('Key'),str('Value')] for i in range(1)]
        metadata.append([str('Name'),fileList[2].rstrip()])
        metadata.append([str('Address Line 1'),fileList[3].rstrip()])
        metadata.append([str('Address Line 2'),fileList[4].rstrip()])
        metadata.append([str('Address Line 3'),fileList[5].rstrip()])
        metadata.append([fileList[22].rstrip(),fileList[24].rstrip()])
        metadata.append([fileList[26].rstrip(),fileList[30].rstrip()])
        metadata.append([fileList[28].rstrip(),fileList[32].rstrip()])
        
        for k in fileList[]:
            
            
