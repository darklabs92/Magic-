# -*- coding: utf-8 -*-
"""
Created on Tue Nov 01 22:47:32 2016

@author: vsdak
"""

import os
import pandas as pd
import numpy as np

# set the working directory
path = "F:/banking/payments/pdf2excel/"
os.chdir(path)
fils2 = os.listdir(path)

def convertMoney(strr):
    strr = str(strr)
    st = ""
    remove = ["$",",","(",")"]
    for l in strr:
        if l not in remove:
            st = st + l
    return float(st)
    

# for each TXT file present in the 'path' folder
for f in fils2:
    if f[-4:]==".txt":
        print f
        ct=0
        n=100000
        # Method 1 to read txt file
        with open(f, 'r') as file:
            fileList = file.readlines()
        # create a 2D matrix detailing the final output structure
        otp = [['Date','Description','Amount'] for i in range(1)]
        # create a metadata 2D matrix detailing the metadata about the CC
        # metadata headers are 'Key' & 'Value'
        metadata = [[str('Key'),str('Value')] for i in range(1)]
        # store the CC customer Name
        metadata.append([str('Name'),fileList[2].rstrip()])
        # store the CC customer's address
        metadata.append([str('Address Line 1'),fileList[3].rstrip()])
        metadata.append([str('Address Line 2'),fileList[4].rstrip()])
        metadata.append([str('Address Line 3'),fileList[5].rstrip()])
        # store the Credit Limit allotted towards the CC
        metadata.append([fileList[22].rstrip(),convertMoney(fileList[24].rstrip())])
        # store the minimum amount due towards the CC for the current month's bill
        metadata.append([fileList[26].rstrip(),convertMoney(fileList[30].rstrip())])
        # store the Due Date for the current month's bill
        metadata.append([fileList[28].rstrip(),fileList[32].rstrip()])
        # store the Date that the current month's bill has been Generated on 
        metadata.append([fileList[28].rstrip(),fileList[32].rstrip()])
        desc = []
        date = []
        amt = []
        for k in range(len(fileList[42:])):
            if fileList[k+42].rstrip()=="REF NO: MB431291141A16":
                # determine the start of transaction descriptions
                n=k
                print "n=",n
                ct=1
            if n<k:
                if fileList[k+43].rstrip()=="":
                    if ct==0:
                        # determine where is the stop of the descriptions
                        print "k=",k             
                        for l in range(n+1,k):
                            desc.append(str(fileList[l+43].rstrip()))
                            ct=0
                     
            
