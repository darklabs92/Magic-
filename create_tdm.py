# -*- coding: utf-8 -*-
"""
Created on Fri Sep 04 21:07:49 2015

@author: aditya
"""

# Store the TermDocumentMatrix function from textmining package in the variable tdm
tdm = textmining.TermDocumentMatrix()

# Now create the TDM. Not that each element in the list, tot_text, created above is a document, relating to each article file in the folder
for text in tot_text:
    tdm.add_doc(text)

# Now the tdm object contains the TDM
# Let's write it to a csv

tdm.write_csv("my_first_tdm.csv")

# This TDM will be really sparse with lots of zero values. Let's find out how sparse the TDM really is. 
#  Here, we encode all the zeroes in the csv file as NaNs (Missing Value in Python)

tdm_df=pd.read_csv('my_first_tdm.csv', na_values = 0)

# Calculate total number of missing values in the data frame
num_missing = tdm_df.isnull().values.ravel().sum()

# Calculate total number of values in the data frame

tot_values = tdm_df.shape[0]*tdm_df.shape[1]

# Calculate the proportion of missing values
missing_prop = num_missing/float(tot_values)
print missing_prop

# Let's now create a TF-IDF
