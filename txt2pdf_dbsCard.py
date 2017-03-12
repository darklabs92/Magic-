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

def checkIfNumeric(arrays):
    valReturn = []
    for i1 in arrays:
        try:
            float(i1.strip())
            valReturn.append(float(i1.strip()))
        except ValueError:
            #print i1, " is Not a float"
            continue
    return valReturn
    

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
        for k2 in range(chk,chk+500):
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
                # store the Grand Total due towards the CC for the current month's bill
                metadata.append(["GRAND TOTAL", convertMoney(fileList[k3+2].strip())])
                break
        ctry = len(fileList)
        for k4 in range(tri, len(fileList)):
            if "DAILY$ AVAILABLE :" in fileList[k4]:
                ctry = k4
                amt = checkIfNumeric(fileList[ctry].split(" "))
                print "Total Daily$ available this month are", amt[0]
                #metadata.append(["TOTAL DAILY$ AVAILABLE ", amt[0]])
                break
        for k5 in range(ctry, len(fileList)):
            if "BALANCE AS OF" in fileList[k5]:
                ctry2 = k5
                ckhFloat = 0
                ckhBrk = 0
                for k6 in range(ctry2, ctry2+20):
                    if len(checkIfNumeric(fileList[k6].split()))>0:
                        ckhFloat = ckhFloat+1
                        if ckhFloat>1:
                            ctry3 = k6
                    else:
                        if fileList[k6]=="\n":
                            if ckhFloat<2:
                                continue
                            else:
                                print f, "Total Daily $ Balance", fileList[ctry3]
                                numToStore = checkIfNumeric(fileList[ctry3].split())[0]
                                # store the Total Daily $ Transactions on the CC for the current month's bill, if the value is less than 1000 dollars
                                # have put this check as the credit card number is also being captured in this process
                                # can resolve it later by checking if the file input / line value is same as credit card no
                                # not done it now as we do not want to capture / store the CC no ANYWHERE! :)
                                if numToStore<1000:
                                    if ckhFloat==2:
                                        # store the Total Daily $ Available on the CC for the current month's bill
                                        metadata.append(["Total DAILY$ Available", numToStore])
                                        print ckhFloat,"Available",checkIfNumeric(fileList[ctry3].split())[0]
                                    elif ckhFloat/2<3:
                                        # store the Total Daily $ Earned on the CC for the current month's bill
                                        metadata.append(["Total DAILY$ Earned ", numToStore])
                                        print ckhFloat, "Earned",numToStore
                                    elif ckhFloat/2<4:
                                        # store the Total Daily $ Redeemed / Adjusted on the CC for the current month's bill
                                        metadata.append(["Total DAILY$ Redeemed / Adjusted", numToStore])
                                        print  ckhFloat,"Redeemed",numToStore
                                    else:
                                        break
                                
                        
                        
                    
                
                #print fileList[ctry]
        numTrans = tri + 1 - (k2 + 2)
        
        for tri2 in range(tri+1,tri+2+numTrans):
            print fileList[tri2].strip(),tri2
            # store the descriptions of the individual transactions
            desc.append(fileList[tri2])
        
        