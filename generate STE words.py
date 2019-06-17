#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 20 10:38:29 2019

@author: jack
"""

import pandas as pd
import numpy as np

import re
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.decomposition import LatentDirichletAllocation as LDA
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer

import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=Warning)


def word_topic(tfidf,solution, wordlist):
# Loading scores for each word on each topic/component.
    words_by_topic=tfidf.T * solution
# Linking the loadings to the words in an easy-to-read way.
    components=pd.DataFrame(words_by_topic,index=wordlist)
    return components
    
    # Extracts the top N words and their loadings for each topic.
def top_words(components, n_top_words):
    n_topics = range(components.shape[1])
    index= np.repeat(n_topics, n_top_words, axis=0)
    topwords=pd.Series(index=index)
    for column in range(components.shape[1]):
        # Sort the column so that highest loadings are at the top.
        sortedwords=components.iloc[:,column].sort_values(ascending=False)
        # Choose the N highest loadings.
        chosen=sortedwords[:n_top_words]
        # Combine loading and index into a string.
        chosenlist=chosen.index +" "+round(chosen,2).map(str) 
        pd.concat([topwords,chosenlist])
    return(chosenlist)

fn="data"
df = pd.read_csv(fn)

lcnt = dcnt = 0
d_paras=[]
l_paras=[]
chosen_list = []
for index,row in df.iterrows():
    if ((row['spirit after'] == 'agnostic') or (row['spirit after'] == 'atheist')):
        dcnt = dcnt +1
        d_paras.append(re.sub("\d+", "", row['detail']))
    else:
        lcnt = lcnt +1
        l_paras.append(re.sub("\d+", "", row['detail']))
print("Items Light:",lcnt,"dark:",dcnt)
    
def get_top_100(data):
    stop_words = (text.ENGLISH_STOP_WORDS)
    my_addit_stop_words =  ["was","just","seeing","away", "felt","saw",\
                            "did","xe","quite","abc", "said","didnt","feel" \
                            "tell","wasnt","really","main","th","im","ive"]
    
    stop_words = stop_words.union(my_addit_stop_words)
    vectorizer = TfidfVectorizer(stop_words=stop_words)
    data_tfidf=vectorizer.fit_transform(data)
    # Getting the word list.
    terms = vectorizer.get_feature_names()
    # Number of topics.
    ntopics=5
    
    # Linking words to topics

# Number of words to look at for each topic.
    n_top_words = 100#10

# LSA
    svd= TruncatedSVD(ntopics)
    lsa = make_pipeline(svd, Normalizer(copy=False))
    data_lsa = lsa.fit_transform(data_tfidf)
    components_lsa = word_topic(data_tfidf, data_lsa, terms)
    chosen_list = top_words(components_lsa, n_top_words)     

# LDA
    lda = LDA(n_topics=ntopics, 
              doc_topic_prior=None, # Prior = 1/n_documents
              topic_word_prior=1/ntopics,
              learning_decay=0.7, # Convergence rate.
              learning_offset=10.0, # Causes earlier iterations to have less influence on the learning
              max_iter=10, # when to stop even if the model is not converging (to prevent running forever)
              evaluate_every=-1, # Do not evaluate perplexity, as it slows training time.
              mean_change_tol=0.001, # Stop updating the document topic distribution in the E-step when mean change is < tol
              max_doc_update_iter=100, # When to stop updating the document topic distribution in the E-step even if tol is not reached
              n_jobs=-1, # Use all available CPUs to speed up processing time.
              verbose=0, # amount of output to give while iterating
              random_state=0)

    data_lda = lda.fit_transform(data_tfidf) 
    components_lda = word_topic(data_tfidf, data_lda, terms)
    x = (top_words(components_lda, n_top_words))
    chosen_list = chosen_list.append(x)

# NNMF
    nmf = NMF(alpha=0.0, 
              init='nndsvdar', # how starting value are calculated
              l1_ratio=0.0, # Sets whether regularization is L2 (0), L1 (1), or a combination (values between 0 and 1)
              max_iter=200, # when to stop even if the model is not converging (to prevent running forever)
              n_components=ntopics, 
              random_state=0, 
              solver='cd', # Use Coordinate Descent to solve
              tol=0.0001, # model will stop if tfidf-WH <= tol
              verbose=0 )# amount of output to give while iterating
    
    data_nmf = nmf.fit_transform(data_tfidf) 
    components_nmf = word_topic(data_tfidf, data_nmf, terms)
    chosen_list = chosen_list.append(top_words(components_nmf, n_top_words))
    x = list(dict.fromkeys(list(chosen_list.index)))
    return(x[:60])

light_words = set(get_top_100(l_paras))
dark_words  = set(get_top_100(d_paras))
print("LIGHT:",light_words)
print("\n\nDARK:",dark_words)
# Equivalent to B-A - print(B.difference(A))
diff = dark_words.difference(light_words)
print("\n\nDiff:",diff,len(diff))

diff = str(diff)
diff = diff[1:-1]
diff = re.sub(",","", diff)
fout = open("dark words.txt", "w")
fout.write(diff)
fout.close() 