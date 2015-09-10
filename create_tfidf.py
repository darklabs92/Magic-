# -*- coding: utf-8 -*-
"""
Created on Fri Sep 04 21:09:45 2015

@author: aditya
"""

import sklearn
import scipy

# Let's build our first TF-IDF model. Calculating tf-idf is not available in NLTK so we'll use another data analysis library, scikit-learn.
from sklearn.feature_extraction.text import TfidfVectorizer

# Creating an easier variable like tfidf and assigning it the function
tfidf = TfidfVectorizer()

# Creating the TF-IDF
tfs = tfidf.fit_transform(tot_text)

# View sample TF-IDF values
tfs.data


# Viewing the tfs object
# The words are assigned numerical values. To get the actual words, use the get_feature_names function

feature_names = tfidf.get_feature_names()

# Print out the Feature Names, the TF-IDF score and the Document Index

for col in tfs.nonzero()[1]:
    print feature_names[col], ' - ', tfs[0, col], ' - ', tfs.indices[col]
    
    
# You can write out your tf-idf into a file. It's a sparse matrix of the type scipy.sparse.csr.csr_matrix, hence, has to be carefully handled
    
scipy.io.mmwrite("tf_idf.mtx", tfs, comment='', field=None, precision=None)

# View the above file in Notepad ++

# You can also change the tf value to always display 1 for a non-zero Term Count. 
# If True, all non-zero term counts are set to 1. 
# This does not mean outputs will have only 0/1 values, only that the tf term in tf-idf is binary 

tfidf_binary = TfidfVectorizer(binary=True)
tfs_binary = tfidf.fit_transform(tot_text)

# View sample TF-IDF values
tfs_binary.data

# Viewing the tfs object
# The words are assigned numerical values. To get the actual words, use the get_feature_names function

feature_names_binary = tfidf.get_feature_names()

# Print out the Feature Names, the TF-IDF score and the Document Index

for col in tfs_binary.nonzero()[1]:
    print feature_names_binary[col], ' - ', tfs_binary[0, col], ' - ', tfs_binary.indices[col]
    
# You can write out your tf-idf into a file. It's a sparse matrix of the type scipy.sparse.csr.csr_matrix, hence, has to be carefully handled
    
scipy.io.mmwrite("tfs_binary.mtx", tfs_binary, comment='', field=None, precision=None)
	
# Let's create some beautiful WordClouds
