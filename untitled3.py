# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 01:48:17 2016

@author: Maria
"""
import json
import nltk
from collections import Counter
from nltk.corpus import stopwords
from nltk.corpus import words

filename = 'yelp_academic_dataset_review_small.json'

tlist =[]

with open(filename) as data_file:    
    data = json.loads(data_file.read())
    
    for x in range(10): #just working with a small subset
    
        reviewText = data[x]['text']
        stars = data[x]['stars']
        
        content = nltk.word_tokenize(reviewText)
        content = [w.lower() for w in content] #normalizing the text
        
        ps = nltk.PorterStemmer()
        content = set([ps.stem(w) for w in content if w in words.words() and w not in stopwords.words("english")]) 
        #filtering out stop words and dashes/ other symbols
        #turn into set to remove duplicate lemmas in the same review

        for word in content: #creates a list of tuples, each tuple contains the lemma and star rating
            t = (word, stars)
            tlist.append(t)
            
    c = Counter(elem[0] for elem in tlist) #counts the occurences of each word
        #returns a dictionary with the word and count but not the star rating
    
    #r = c.pop(elem[0] for elem in c if c.get(elem[0]) < 10)
    #tried to remove the ones occuring less than 10 times but it crashes there
    
    print(c)              
 
    