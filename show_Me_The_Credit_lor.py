# -*- coding: utf-8 -*-
"""
Created on Fri Apr 06 00:47:58 2017

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
import sklearn
from sklearn.feature_selection import RFE, SelectKBest, chi2
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import ExtraTreesClassifier
from sklearn import metrics


# set the path where the files are stored
path = "F:/Kaggle/honestbee_credit/"

os.chdir(path)

fls = os.listdir(path)

# read in the train DS (data set) specifically
trainPd = pd.read_csv(path+"cs-training.csv", header=0)

testPd = pd.read_csv(path+"cs-test.csv", header=0)

trainPd.columns

# observed that the names did not change despite changes made in the CSV
# hence, change the names explicitly below
cols = ['id','seriousDlq2yr','revolvngUnsecuredUtilised','age',
                   'num30to59only','debtRatio','monthlyIncm','numOpenCrdNLoan',
                   'num90aab','numFixedLines','num60to89only','fmlyMembrs']

trainPd.columns = cols

testPd.columns = cols

###
# Initial data exploration and data sanity checks 
###

# get an overview of data set and which are there any basic problems
trainPd.describe()

testPd.describe()

# if mean ~ median, progrnosis = normally distributed
#   revolvngUnsecuredUtilised should ONLY lie b/w 0 and 1, yet it has a max value of 50708
#   monthlyIncome and fmlyMembrs have a lot of NaNs 
#   

### id the problematic fields 

# train - Revolve Utilisation
revolvIndx = list(trainPd.loc[:,'revolvngUnsecuredUtilised']>1.0)
revolveGrtrThn1 = [rw for rw in range(len(revolvIndx)) if revolvIndx[rw]==True]
    # 3321 [2.214%] records are more than 1 - which is impossible
len(revolveGrtrThn1)

# test - Revolve Utilisation
testRevolvIndx = list(testPd.loc[:,'revolvngUnsecuredUtilised']>1.0)
testRevolveGrtrThn1 = [rw for rw in range(len(testRevolvIndx)) if testRevolvIndx[rw]==True]
    # 2181 [2.15%] records are more than 1 - which is impossible
len(testRevolveGrtrThn1 )


# train - Debt Ratio
debtRatioIndx = list(trainPd.loc[:,'debtRatio']>1.0)
dRGrtrThn1 = [rw for rw in range(len(debtRatioIndx)) if debtRatioIndx[rw]==True]
#dRvals = list(trainPd.loc[:,'debtRatio'])
#dRcorrectVals = [k for k in range(len(dRvals)) if k not in dRGrtrThn1]
#dRvals2 = dRvals.copy()
    # 32137 [21.42%] records are more than 1 - which is impossible
len(dRGrtrThn1)

# test - Debt Ratio
testDRvals = list(testPd.loc[:,'debtRatio'])

testDebtRatioIndx = list(testPd.loc[:,'debtRatio']>1.0)
testDRGrtrThn1 = [rw for rw in range(len(testDebtRatioIndx)) if testDebtRatioIndx[rw]==True]
#dRcorrectVals = [k for k in range(len(dRvals)) if k not in dRGrtrThn1]
#dRvals2 = dRvals.copy()
    # 23578 records [23.23%] are more than 1 - which is supposed to be quite rare, if not impossible
len(testDRGrtrThn1)


# train - Family Members
fmlyMem = list(trainPd.loc[:,'fmlyMembrs'])
fmlyMembrIndx = [rw for rw in range(len(fmlyMem)) if str(fmlyMem[rw])[2]!='0']
    # 3931 [2.62%] are either nan or deciaml values - which are possibly wrong
len(fmlyMembrIndx)

# test - Family Members
testFmlyMem = list(testPd.loc[:,'fmlyMembrs'])
testFmlyMembrIndx = [rw for rw in range(len(testFmlyMem)) if str(testFmlyMem[rw])[2]!='0']
    # 2631 [2.59%] are either nan or deciaml values - which are possibly wrong
len(testFmlyMembrIndx)


# train - Monthly Incm
mnthIncm = list(trainPd.loc[:,'monthlyIncm'])
mnthIncmIndx = [rw for rw in range(len(mnthIncm)) if math.isnan(mnthIncm[rw])==True or mnthIncm[rw]==0]
    # 31365 [20.91%] are either nan or deciaml values - which are possibly wrong
len(mnthIncmIndx)

# test - Monthly Incm
testMnthIncm = list(testPd.loc[:,'monthlyIncm'])
testMnthIncmIndx = [rw for rw in range(len(testMnthIncm)) if math.isnan(testMnthIncm[rw])==True or testMnthIncm[rw]==0]
    # 21123 [20.81%] are either nan or deciaml values - which are possibly wrong
len(testMnthIncmIndx)

# these are abnormal values - each lst holds records with values above 1
rmvIndx2 = []
for z in revolveGrtrThn1:
    if z in dRGrtrThn1:
        rmvIndx2.append(z)

# these are missing & abnormal values - each lst holds records with values including, but not limited to, nans; hence considered seperately
rmvIndx3 = []
for z in fmlyMembrIndx:
    if z in mnthIncmIndx:
        rmvIndx3.append(z)

len(rmvIndx2)
len(rmvIndx3)

rmv2 = []
for z in rmvIndx2:
    if z in rmvIndx3:
        rmv2.append(z)


rmv = list(np.unique(rmvIndx2))
len(rmv)



# remove the rows which are quite problematic

trainDumpFmly = trainPd[np.isfinite(trainPd['fmlyMembrs'])]
testDumpFmly = testPd[np.isfinite(testPd['fmlyMembrs'])]

# determine how many NULL values exist across Train & Test DS
#train
colNullCnt = []

for z in range(len(cols)):
    colNullCnt.append([cols[z], sum(pd.isnull(trainPd[cols[z]]))])

colNullCnt

#test
colNullCnt2 = []

for z in range(len(cols)):
    colNullCnt2.append([cols[z], sum(pd.isnull(testPd[cols[z]]))])

colNullCnt2

# Impute the missing values with the mean of each col
trainPd_fild = trainPd.fillna(math.ceil(trainPd.mean()), inplace = False)
testPd_fild = testPd.fillna(math.ceil(testPd.mean()), inplace = False)


# view how each variable is distributed and come up with initial prognosis
for z2 in range(len(cols)):
    print cols[z2]
    trainPd_fild[cols[z2]].plot.box()
    fig = plt.figure()
    trainPd_fild[cols[z2]].plot.hist()
    plt.show()
    #trainPd.plot.scatter(y='seriousDlq2yr', x=cols[z2])
    print ""

#scatter_matrix(trainPd, alpha=0.5, figsize=(12, 12), diagonal='kde')


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
# so, for now, let us use a simple mean of EACH COL (line 63: trainPd_fild)

# basic avg training set
trainPd__fild_indpndnt = trainPd_fild[trainPd_fild.columns.difference(['seriousDlq2yr', 'id'])].copy()
trainPd__fild_dpndnt = trainPd_fild['seriousDlq2yr'].copy()

# training_ds

testPd_inp = testPd_fild[testPd_fild.columns.difference(['seriousDlq2yr', 'id'])]
testPd_outp = testPd_fild[['id','seriousDlq2yr']].copy()

msk = np.random.rand(len(trainPd__fild_indpndnt)) < 0.8

model = LogisticRegression()
# create the RFE model and select 3 attributes
rfe = RFE(model, 5)
rfe = rfe.fit(trainPd__fild_indpndnt, trainPd__fild_dpndnt)

print(rfe.support_)
print(rfe.ranking_)

for e in range(len(list(rfe.ranking_))):
    print rfe.ranking_[e]
    print rfe.support_[e]
    print trainPd__fild_indpndnt.columns[e]
    print ""


modelLog = LogisticRegression()
modelLog.fit_transform(trainPd__fild_indpndnt, trainPd__fild_dpndnt)
testPd_outp['seriousDlq2yr'] = modelLog.predict(testPd_inp)
testPd_outp.columns = ['Id','Probability']
#testPd_outp.to_csv(path+"try1.csv", header=True, index=False)

# decision tree
# naive bayes
# ensemble

test = SelectKBest(score_func=chi2, k=5)
fit = test.fit(trainPd__fild_indpndnt, trainPd__fild_dpndnt)

for z in range(len(fit.scores_)):
    print z, fit.scores_[z], trainPd__fild_indpndnt.columns[z], fit.get_support()[z]

train_ind_4select = trainPd_fild[['debtRatio','monthlyIncm','num60to89only','num90aab']].copy()

test_ind_4select = testPd_fild[['debtRatio','monthlyIncm','num60to89only','num90aab']].copy()

modelLog = LogisticRegression()
modelLog.fit_transform(train_ind_4select, trainPd__fild_dpndnt)
testPd_outp['seriousDlq2yr'] = modelLog.predict(test_ind_4select )
testPd_outp.columns = ['Id','Probability']
testPd_outp.to_csv(path+"try1_select4best_chi.csv", header=True, index=False)


np.set_printoptions(precision=3)
print(fit.scores_)
features = fit.transform(trainPd__fild_indpndnt)
# summarize selected features
print(features[0:5,:])

model = ExtraTreesClassifier()
model.fit(trainPd__fild_indpndnt, trainPd__fild_dpndnt)
# display the relative importance of each attribute
print(model.feature_importances_)

for z in range(len(model.feature_importances_)):
    print z, trainPd__fild_indpndnt.columns[z], model.feature_importances_[z]


    
#model.fit(dataset.data, dataset.target)

#expected = dataset.target

#predicted = model.predict(dataset.data)
    
#print(metrics.classification_report(expected, predicted))

#print(metrics.confusion_matrix(expected, predicted))