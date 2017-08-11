# -*- coding: utf-8 -*-
"""
Created on Sat Aug 12 02:46:39 2017

@author: vsdaking
"""

import pandas as pd
import numpy as np
import time
import os
from bs4 import BeautifulSoup
from datetime import datetime 
import requests
import itertools
import math
import dryscrape

print "Extract data from HWZ Forums"

urlList = ["http://www.hardwarezone.com.sg/search/all/", "http://www.hardwarezone.com.sg/tag-search/all/"]

txt2search = str(raw_input("Please provide us the key terms to search for \n"))

indWords = [k1.strip() for k1 in txt2search.strip().split(" ")]

ct=0
finWords = []
for k in range(len(indWords)+1):
    for k1 in itertools.permutations(indWords,k):
        if len(k1)<1:
            continue
        print k1
        finWords.append(' '.join(k1))
        if len(k1)==len(indWords):
            ct=1
        if ct==1:
            break
            
print "We have been provided "+txt2search + " as input and it comprises "+ str(len(indWords)) + " individual words."
print "However, we will be searching for the following ",str(len(finWords)),"words"
print finWords

pth = "D:/vd/hwz_scraped/"
if not os.path.exists(pth):
    os.makedirs(pth)
    print pth, "has been created"
else:
    os.chdir(pth)
    print pth, "exists"

globalDf = pd.DataFrame()

## Scraping process
for word in finWords:
    url_Search_Term = "+".join(word.split(" "))
    if url_Search_Term.isdigit()==True:
        continue
    elif url_Search_Term.lower().strip() == "nan":
        continue
    url = urlList[0]+url_Search_Term
    print url
    r  = requests.get(url)
    
    data = r.text
    data2 = data.replace('\n','')
    
    soup = BeautifulSoup(data2.text)
    
    
    tblRaw2 = soup.find("div", {"class":"st-text"})
    
    print tblRaw2.prettify()
    print ""
    print [x.contents[0] for x in tblRaw2.find_all('a')]
    print ""         
    
    allProducts = [x.contents[0] for x in tblRaw2.find_all('a')]
                   
    p = pd.DataFrame(allProducts, columns = ['All_Brands'])
    p.to_csv('All_brands.csv', header=True, index=False)
