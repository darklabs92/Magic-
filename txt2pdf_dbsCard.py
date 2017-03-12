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
        #print f
        ct=0
        n=100000
        # Method 1 to read txt file
        with open(f, 'r') as file:
            fileList = file.readlines()
        # create a 2D matrix detailing the final output structure
        otp = [['Date','Description','Amount'] for i in range(1)]
        
        
        ## create a metadata 2D matrix detailing the metadata about the CC
        
        # metadata headers are 'Key' & 'Value'
        metadata = [[str('Key'),str('Value')] for i in range(1)]
        
        # store the CC customer Name
        metadata.append([str('Name'),fileList[2].rstrip()])
        
        # extract the customer's complete Address
        add = ""
        for k in range(3, len(fileList)):
            if "DBS Bank Ltd" not in fileList[k]:
                if fileList[k]!="\n":
                    add = add + fileList[k].strip()+", "
            else:
                break
            
        # store the CC customer's address
        metadata.append([str('Address'),add[:len(add)-2]])
        
        ind = k+5
        for pos in range(ind,ind+50):
            if "STATEMENT DATE" in fileList[pos]:
                # store the Date that the current month's bill has been Generated on
                metadata.append(["STATEMENT DATE",fileList[pos+2].rstrip()])
            
            if "PAYMENT DUE DATE" in fileList[pos]:
                # store the Due Date for the current month's bill
                metadata.append(["PAYMENT DUE DATE",fileList[pos+4].rstrip()])
                break
            
            if "CREDIT LIMIT" in fileList[pos]:
                # store the Credit Limit allotted towards the CC
                metadata.append(["CREDIT LIMIT",convertMoney(fileList[pos+2].rstrip())])
            
            if "MINIMUM PAYMENT" in fileList[pos]:
                # store the minimum amount due towards the CC for the current month's bill
                metadata.append(["MINIMUM PAYMENT",convertMoney(fileList[pos+4].rstrip())])
                
        desc = []
        date = []
        amt = []
        
        ## determine the start of transaction descriptions        
        for k in range(pos,len(fileList)):
            if "REF NO:" in fileList[k].rstrip():
                chk = k
                print "Transactions begin from line",k+1
                break
        for k2 in range(chk,chk+250):
            if "NEW TRANSACTIONS" in fileList[k2]:
                print "Dates of Transactions begin from line",k2+2
                break
        for tri in range(k2, len(fileList)):
            if fileList[tri]!="\n":
                # store the dates of the individual transactions
                date.append(fileList[tri].strip())
            else:
                print "Dates of Transactions end at line",tri
                break
        for k3 in range(tri,len(fileList)):
            if "GRAND TOTAL FOR" in fileList[k3]:
                print "Total Amount Payable is",fileList[k3+2].strip()
                metadata.append(["GRAND TOTAL", convertMoney(fileList[k3+2].strip())])
                break
        numTrans = tri + 1 - (k2 + 2)
        
        for tri2 in range(tri+1,tri+2+numTrans):
            print fileList[tri2].strip(),tri2
            # store the descriptions of the individual transactions
            desc.append(fileList[tri2])
        
        