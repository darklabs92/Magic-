# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 00:49:43 2017

@author: darkDawg
"""
## this program takes given .xlsx docs, applies Stanford NER to the same and outputs the NEs thus found alongside the type of entity


# import all requisite packages
import os
import sys
import nltk
from nltk import *
import string
import numpy as np
import pandas as pd
from nltk.tokenize import sent_tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time
from collections import Counter
from nltk.corpus import stopwords
import copy


# Check if stanford.py file exists
import distutils.sysconfig
print distutils.sysconfig.get_python_lib()+'/nltk/tag/'
# Go to the above path and check


# Import POSTagger and NERTagger from nltk.tag.stanford
from nltk.tag.stanford import POSTagger
from nltk.tag.stanford import NERTagger


# Set JAVAHOME variable as below
import os
java_path = "C:/Program Files (x86)/Java/jre1.8.0_51/bin/java.exe"
os.environ['JAVAHOME'] = java_path


    
# Point to the directory holding the models and the directory holding the jar file for the stanford pos tagger. An example is shown below
POS_Tagger_path = "D:/training/NER/Stanford_setup_adi/Stanford-20160909T053823Z/Stanford/stanford-postagger-full-2014-08-27/stanford-postagger-full-2014-08-27/"

st=POSTagger(POS_Tagger_path + "models/english-bidirectional-distsim.tagger", POS_Tagger_path + "stanford-postagger.jar")

# Point to the directory holding the models and the directory holding the jar file for the stanford pos tagger. An example is shown below
NER_Tagger_path = "D:/training/NER/Stanford_setup_adi/Stanford-20160909T053823Z/Stanford/stanford-ner-2015-04-20/stanford-ner-2015-04-20/"

english_nertagger = NERTagger(NER_Tagger_path  + 'classifiers/english.all.3class.distsim.crf.ser.gz', NER_Tagger_path  + 'stanford-ner.jar')


path1 = "F:/datasets/social_at_ogilvy/"

path1 = "D:/vd/banking/Social - Data Test Brief package/"

os.chdir(path1)

os.listdir(path1)

bigPd = pd.ExcelFile("test data 1 - social listening (Huawei)_v1.1.xlsx")

finPd = pd.DataFrame()
for sheetName in  bigPd.sheet_names:
    if sheetName!='Sheet1':
        countryPd = bigPd.parse(sheetname = sheetName,header = 8)
        print sheetName
        print countryPd.columns
        print countryPd.shape, len(countryPd.columns)
        countryPd['country']=sheetName
        #countryPd.to_csv(sheetName+".csv", header=True, index=False)
        finPd = pd.concat([finPd, countryPd])

content = np.array(finPd.Content_new)
content2 = list()
for i in content:
    if type(i)==float:
        content2.append(str(i))
    else:
        content2.append(i.encode('utf-8', 'ignore').decode('utf-8').encode('ascii', 'ignore').decode('ascii').strip('\n'))

analyzer = SentimentIntensityAnalyzer()
finPd.Content_new = pd.Series(content2)
finMtrx = finPd.as_matrix()

# feature engineering
# generate new features from existing fields
# first, create a structure to hold all this data
finMtrx2 = np.ndarray(shape = (finMtrx.shape[0], finMtrx.shape[1]+7), dtype = np.ndarray)

# 7 new fields represent:
    # 1. Compound sentiment score
    # 2. Neutral sentiment score
    # 3. Negative sentiment score
    # 4. Positive sentiment score
    # 5. Other Mobile Brands spoken of
    # 6. Is Huawei or it's products mentioned?
    # 7. Product the content is targeted towards
    # 8. 
    
finMtrx2[:,:finMtrx.shape[1]] = finMtrx
for sentence in range(len(content2)):
    vs = analyzer.polarity_scores(content2[sentence])
    finMtrx2[sentence][finMtrx.shape[1]] = vs['compound']
    finMtrx2[sentence][finMtrx.shape[1]+1] = vs['neu']
    finMtrx2[sentence][finMtrx.shape[1]+2] = vs['neg']
    finMtrx2[sentence][finMtrx.shape[1]+3] = vs['pos']
    
mtrxCols = copy.deepcopy(finPd.columns)
mtrxCols = list(mtrxCols) + list(['compound','neutral','negative','positive'])




#from external.my_potts_tokenizer import MyPottsTokenizer
review = content2
def get_sentences(review):
    """
    INPUT: full text of a review
    OUTPUT: a list of sentences
    Given the text of a review, return a list of sentences. 
    """

    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    post_stnfrd_tag = []
    aspects_stnfrd = []
    for u in range(len(review)):
        x = review[u]
        print "This is ",u
        sentenced = sent_detector.tokenize(x)
        #post_def_tag = []
        #aspects_def = []
        stnfrd_tag = []
        ct=0
        for sent in sentenced:
            print sent
            #default_tag = pos_tag(sent)
            #print default_tag
            stnfrd_tag.extend(pos_tag_stanford(sent))
            #print ""
            print "Stanford", u,str(ct + 1)
            #print ""
            print "Stanford Tag is",stnfrd_tag
            ct+=1
            #post_def_tag.append(default_tag)
        post_stnfrd_tag.append(stnfrd_tag)
        #aspects_def.append([aspects_from_tagged_sents(default_tag)])
        aspects_now = aspects_from_tagged_sents(stnfrd_tag)
        aspects_stnfrd.append(aspects_now)
        print len(stnfrd_tag), len(post_stnfrd_tag)
        stnfrd_tag = []
        print len(aspects_now), len(aspects_stnfrd)
    #return post_def_tag, aspects_def, post_stnfrd_tag, aspects_stnfrd   
    return post_stnfrd_tag, aspects_stnfrd   
          

def tokenize(sentence):
	"""
	INPUT: string (full sentence)
	OUTPUT: list of strings
	Given a sentence in string form, return 
	a tokenized list of lowercased words. 
	"""

	pt = [k.lower() for k in nltk.sent_tokenize(sentence)]
	return pt


def pos_tag(toked_sentence):
	"""
	INPUT: list of strings
	OUTPUT: list of tuples
	Given a tokenized sentence, return 
	a list of tuples of form (token, POS)
	where POS is the part of speech of token
	"""
	return nltk.pos_tag(toked_sentence.split(' '))


def pos_tag_stanford(toked_sentence):
    """
    INPUT: list of strings
    OUTPUT: list of tuples
    Given a tokenized sentence, return 
    a list of tuples of form (token, POS)
    where POS is the part of speech of token
    """
    
    from nltk.tag.stanford import POSTagger
 
    
    POS_Tagger_path = "D:/training/NER/Stanford_setup_adi/Stanford-20160909T053823Z/Stanford/stanford-postagger-full-2014-08-27/stanford-postagger-full-2014-08-27/"
    
    # Point to the directory holding the models and the directory holding the jar file for the stanford pos tagger. An example is shown below
    st=POSTagger(POS_Tagger_path + "models/english-bidirectional-distsim.tagger", POS_Tagger_path + "stanford-postagger.jar")

    NER_Tagger_path = "D:/training/NER/Stanford_setup_adi/Stanford-20160909T053823Z/Stanford/stanford-ner-2015-04-20/stanford-ner-2015-04-20/"

    # Point to the directory holding the models and the directory holding the jar file for the stanford pos tagger. An example is shown below
    english_nertagger = NERTagger(NER_Tagger_path  + 'classifiers/english.all.3class.distsim.crf.ser.gz', NER_Tagger_path  + 'stanford-ner.jar')
 
    return st.tag(toked_sentence.split(' ')), 
    entity = []
    for sent2 in nltk.sent_tokenize(toked_sentence):
        entity.append([(k,type1) for (k,type1) in english_nertagger.tag(word_tokenize(sent2)) if type1!='O'])


def aspects_from_tagged_sents(tagged_sentences):
	"""
	INPUT: list of lists of strings
	OUTPUT: list of aspects
	Given a list of tokenized and pos_tagged sentences from reviews
	about a given restaurant, return the most common aspects
	"""

	STOPWORDS = set(stopwords.words('english'))

	# find the most common nouns in the sentences
	noun_counter = Counter()

	print "Received for aspects extraction is ",len(tagged_sentences)

	for sent2 in tagged_sentences:
		print "Sent is ",sent2, len(sent2)
		for word, pos in sent2: 
		    if pos=='NNP' or pos=='NN' and word not in STOPWORDS:
			    noun_counter[word] += 1

	# list of tuples of form (noun, count)
	return [noun for noun, _ in noun_counter.most_common(10)]


def demo_aspect_extraction(): 
	"""
	Demo the aspect extraction functionality on one restaurant
	""""""x
	from main import read_data, get_reviews_for_business, extract_aspects

	TEST_BIZ_ID = 's1dex3Z3QoqiK7V-zXUgAw'

	print "Reading data..."
	df = read_data()
	print "Done."

	BIZ_NAME = str(df[df.business_id==TEST_BIZ_ID]['name'].iloc[0])


	print "Getting reviews for %s (ID = %s)" % (BIZ_NAME, TEST_BIZ_ID)
	reviews = get_reviews_for_business(TEST_BIZ_ID, df)
	print "Done." """
	print "Extracting aspects..."
	#def_posTag,def_aspects,stnfrd_posTag, stnfrd_aspects = get_sentences(content2[:4])
	startTime = time.time()
	stnfrd_posTag, stnfrd_aspects = get_sentences(content2[:10])
	endTime = time.time()
	np.savetxt("D:/vd/banking/Social - Data Test Brief package/huawei_ver2.csv",finMtrx2, fmt="%s", delimiter=",") 
	stanford = pd.DataFrame([stnfrd_posTag,stnfrd_aspects])
	stanford.to_csv("D:/vd/banking/Social - Data Test Brief package/huawei_stnfrd.csv", header=False, index=False)
	print "Done."+ "Took " +str(endTime-startTime)
	"""
      print "==========="
	print "Aspects for s:"
	for i,aspect in enumerate(stnfrd_aspects):
         print str(i) + ". "
         print aspect
         """
         
demo_aspect_extraction()
