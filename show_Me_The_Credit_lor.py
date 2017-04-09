# -*- coding: utf-8 -*-
"""
Created on Fri Apr 06 00:47:58 2017

@author: vsdaking
"""

###
# Intial Environment setup and reading of files
###

# Aim of program is to predict people most likely to default on their payment,
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
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn import metrics
from sklearn.metrics import roc_auc_score


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
#   debtRatio should ONLY  lie b/w 0 and 1, yet it has a max value of 329664
#   monthlyIncome and fmlyMembrs have a lot of NaNs(determined by difference in count of their records and that of DF)

## determine how many NULL values exist across Train & Test DS
# train
colNullCnt = []

for z in range(len(cols)):
    colNullCnt.append([cols[z], sum(pd.isnull(trainPd[cols[z]]))])

colNullCnt

#test
colNullCnt2 = []

for z in range(len(cols)):
    colNullCnt2.append([cols[z], sum(pd.isnull(testPd[cols[z]]))])

colNullCnt2


## id the problematic fields

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

###
# there is also the case where there are records having multiple entries (i.e. > 0) in either 2 or 3 of the date related cols
# these entries indicate wrong entries / tampering with the data, hence require attention too!
# however, due to the man hour constraints, will devote time to other areas of the problem
###

# list of final Indices to remove - they cause problems in ALL of the columns above!
rmv = list(np.unique(rmv2))
len(rmv)

# remove these rows from trainPd to have a cleaner DS to train on 
trainPd.drop(trainPd.index[rmv2])

## Above, we have tried to clean up the rows of the DS (1 of the dimensions)
## Now, update the columnar contents (2nd dimension) to reflect cleaner DS for further training
#

# we hereby learn that possibly one of the most critical variables - monthly income - almost has 
# a staggering 20% values as missing / NaN!
# this leads me to question how much more dirty is this data ..?
# depending on each scenario, we can determine how to proceed - 
#   1. impute the values via simple stats (mean, median, mode, etc.)
#   2. predict the values based on other factors
#   3. discard the record altogether, as this brings in questions of data integrity (how do we know how valid / correct is the rest of that given entry?!)
#   4. use a filler / predetermined value in place of the missing values
# given the huge no of missing vals, we can rule out option 3 as it will greatly decrease our # of training records
# also, since quite a few of these may be impactful variables, it may not be in our best interests to use a fixed val for the widely varying range of data points (records) we have
# so, for now, let us use a simple mean of EACH COL

# this function helps to cleanse the columns found problematic above - for trainPd and testPd
def cleanUpDFcols(colName, colProblemIndx, testColProblemIndx):
    trainCol = list(trainPd[[colName]].values.flatten())
    print "finished with flattening input column for ", colName 
    tmpGoodValLst = [trainCol[z2] for z2 in range(len(trainCol)) if z2 not in colProblemIndx]
    print "finished with tmpGoodValLst for ", colName 
    avgGoodColVals = np.average(tmpGoodValLst)
    finalLstVals = []
    for s in range(len(trainCol)):
        if s not in colProblemIndx:
            finalLstVals.append(trainCol[s])
        else:
            if colName=='fmlyMembrs':
                finalLstVals.append(math.ceil(avgGoodColVals))
            else:
                finalLstVals.append(avgGoodColVals)
    print "starting with TrainPd for ", colName 
    trainPd[[colName]] = pd.Series(finalLstVals, index = trainPd.index)
    print "finished with TrainPd for ", colName 
    
    testTrainCol = list(testPd[[colName]].values.flatten())
    print "finished with flattening input column for ", colName 
    testTmpGoodValLst = [testTrainCol[z2] for z2 in range(len(testTrainCol)) if z2 not in testColProblemIndx]
    print "finished with testTmpGoodValLst for ", colName 
    testAvgGoodColVals = np.average(testTmpGoodValLst)
    testFinalLstVals = []
    for s2 in range(len(testTrainCol)):
        if s2 not in testColProblemIndx:
            testFinalLstVals.append(testTrainCol[s2])
        else:
             if colName=='fmlyMembrs':
                testFinalLstVals.append((math.ceil(testAvgGoodColVals)))
             else:
                testFinalLstVals.append(testAvgGoodColVals)
    print "starting with TestPd for ", colName 
    testPd[[colName]] = pd.Series(testFinalLstVals, index = testPd.index)
    print "finished with TestPd for ", colName
    return tmpGoodValLst, testTmpGoodValLst
    

for z in range(len(cols)):
    if cols[z]=='revolvngUnsecuredUtilised':
        revolv_goodVals_Train, revolv_goodVals_Test = cleanUpDFcols('revolvngUnsecuredUtilised', revolveGrtrThn1, testRevolveGrtrThn1)
    elif cols[z] == 'debtRatio':
        dR_goodVals_Train, dR_goodVals_Test = cleanUpDFcols('debtRatio', dRGrtrThn1, testDRGrtrThn1)
    elif cols[z] == 'fmlyMembrs':
        fM_goodVals_Train, fM_goodVals_Test = cleanUpDFcols('fmlyMembrs', fmlyMembrIndx, testFmlyMembrIndx)
    elif cols[z] == 'monthlyIncm':
        inc_goodVals_Train, inc_goodVals_Test = cleanUpDFcols('monthlyIncm', mnthIncmIndx, testMnthIncmIndx)
    else:
        continue
        

# engineer some new features
balanceIncomeLeft_train = []
balanceIncomeLeft_test = []

debtRatio_train = list(trainPd.debtRatio)
monthlyInc_train = list(trainPd.monthlyIncm)
debtRatio_test = list(testPd.debtRatio)
monthlyInc_test = list(testPd.monthlyIncm)


for rw2 in range(len(trainPd)):
    balanceIncomeLeft_train.append((1.0 - debtRatio_train[rw2])*monthlyInc_train[rw2])
    
for rw3 in range(len(testPd)):
    balanceIncomeLeft_test.append((1.0 - debtRatio_test[rw3])*monthlyInc_test[rw3])

testPd['balanceIncome'] = pd.Series(balanceIncomeLeft_test, index = testPd.index, dtype=np.float64)
trainPd['balanceIncome'] = pd.Series(balanceIncomeLeft_train, index = trainPd.index, dtype=np.float64)


# Impute the missing values with the mean of each col
trainPd_fild = copy.copy(trainPd)
testPd_fild = copy.copy(testPd)


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




# training_ds
trainPd_indpndnt = trainPd[trainPd.columns.difference(['seriousDlq2yr', 'id'])].copy()
trainPd_dpndnt = trainPd['seriousDlq2yr'].copy()

msk = np.random.rand(len(trainPd_indpndnt)) < 0.8

trainPd_indpndnt_train = trainPd_indpndnt[msk]
trainPd_indpndnt_test = trainPd_indpndnt[~msk]
trainPd_dpndnt_train = trainPd_dpndnt[msk]
trainPd_dpndnt_test = trainPd_dpndnt[~msk]


# testing_ds
testPd_inp = testPd[testPd.columns.difference(['seriousDlq2yr', 'id'])]
testPd_outp = testPd[['id','seriousDlq2yr']].copy()



###
# Build the different models which shall be used
###

##
# Logistic Regression on all independent variables
modelLog = LogisticRegression()
modelLog.fit_transform(trainPd_indpndnt_train, trainPd_dpndnt_train)

pred = modelLog.predict(trainPd_indpndnt_test)
roc_auc_score(trainPd_dpndnt_test, pred)

testPd_outp.columns = ['Id','Probability']
testPd_outp['Probability'] = modelLog.predict(testPd_inp)
testPd_outp.to_csv(path+"try2.csv", header=True, index=False)

# decision tree
# naive bayes
# ensemble


# Logistic Regression on top 4 significant variables (determined via Chi-Sq.)
#
test = SelectKBest(score_func=chi2, k=5)
fit = test.fit(trainPd_indpndnt, trainPd_dpndnt)

for z in range(len(fit.scores_)):
    print z, fit.scores_[z], trainPd_indpndnt.columns[z], fit.get_support()[z]

train_ind_4select = trainPd_fild[['debtRatio','balanceIncome','num60to89only','num90aab']].copy()

test_ind_4select = testPd_fild[['debtRatio','balanceIncome','num60to89only','num90aab']].copy()

modelLog = LogisticRegression()
modelLog.fit_transform(train_ind_4select, trainPd_dpndnt)

pred = modelLog.predict(trainPd_indpndnt_test)
roc_auc_score(trainPd_dpndnt_test, pred)

print(metrics.classification_report(trainPd_dpndnt_test, pred))
print(metrics.confusion_matrix(trainPd_dpndnt_test, pred))



testPd_outp['seriousDlq2yr'] = modelLog.predict(test_ind_4select )
testPd_outp.columns = ['Id','Probability']
testPd_outp.to_csv(path+"try2_select4best_chi.csv", header=True, index=False)


np.set_printoptions(precision=3)
print(fit.scores_)
features = fit.transform(trainPd_indpndnt)
# summarize selected features
print(features[0:5,:])


# Determine the significant variables determined via usage of Extended Tree Classifiers
#
model = ExtraTreesClassifier()
model.fit(trainPd_indpndnt, trainPd_dpndnt)
# display the relative importance of each attribute
print(model.feature_importances_)

for z in range(len(model.feature_importances_)):
    print z, trainPd_indpndnt.columns[z], model.feature_importances_[z]


# Random Forest (RF) Classifier on all input variables - reduces variance and bias
#
train_ind_rndmSelect = trainPd_fild[['debtRatio','monthlyIncm','num60to89only','num90aab']].copy()
train_dep_rndmSelect = trainPd_fild[['seriousDlq2yr']].copy()

trainPd_indpndnt_train = train_ind_rndmSelect[msk]
trainPd_indpndnt_test = train_ind_rndmSelect[~msk]
trainPd_dpndnt_train = train_dep_rndmSelect[msk]
trainPd_dpndnt_test = train_dep_rndmSelect[~msk]

test_ind_rndmSelect = testPd_fild[['debtRatio','monthlyIncm','num60to89only','num90aab']].copy()




modelRFC = RandomForestClassifier()
modelRFC.fit(trainPd_indpndnt_train, trainPd_dpndnt_train)

pred = modelRFC.predict(trainPd_indpndnt_test)
roc_auc_score(trainPd_dpndnt_test, pred)

print(metrics.classification_report(trainPd_dpndnt_test, pred))
print(metrics.confusion_matrix(trainPd_dpndnt_test, pred))

testPd_outp['seriousDlq2yr'] = model.predict(test_ind_rndmSelect)
testPd_outp.columns = ['Id','Probability']
testPd_outp.to_csv(path+"try3_RF.csv", header=True, index=False)

# eval criteria for RFC model
modelRFC.criterion
    
#model.fit(dataset.data, dataset.target)

#expected = dataset.target

#predicted = model.predict(dataset.data)
    
#print(metrics.classification_report(expected, predicted))

#print(metrics.confusion_matrix(expected, predicted))

