# -*- coding: utf-8 -*-
"""
Created on Sat Apr 09 13:22:33 2016

@author: Vidyut
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Apr 08 15:12:26 2016

@author: Vidyut
"""
import pandas as pd
from flask import *
import os
import csv

os.chdir('F:/iSentia/FinalProgram/')
pd.set_option('display.max_colwidth', -1)

p=[]
with open('store_id.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        p.append(row)

f3 = pd.DataFrame(p[1:])
f3.columns = ['ID','Merchant Name']

p2=[]
with open('refer.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        p2.append(row)

f4 = pd.DataFrame(p2[1:])
f4.columns = ['ID','Link']

f7 = f6 = pd.DataFrame()

f7 = pd.merge(f3,f4,how='left',on='ID')
l=1
f6 = pd.DataFrame(f7.Link[l:(l+5)])

sp = []
for i in range(5):
    sp.append(f6.Link[l+i])

f6 = pd.DataFrame(sp)

print ("\nRunning the web UI")

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'
#sess = Session()

@app.route('/')
def hello_world():
    k = f6.to_html(header=False,index=False, escape=False)
    k = Markup(k)
    return render_template('t2.html',k=k)

if __name__ == '__main__':
    app.run()