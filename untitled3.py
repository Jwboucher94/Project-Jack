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
import os.path
import csv

filename = 'yelp_academic_dataset_review_small.json'
ratingcsv = 'rating.csv'

if not os.path.isfile(ratingcsv): #create the teachers.csv file, if not already created
    header = ["Lemma Word", "Lemma Rating"]
    print("Creating rating.csv to store data")
    with open(ratingcsv, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
else: 
    print("Recreating rating.csv...")
    os.remove(ratingcsv)
    header = ["Positive Lemma", "Negative Lemma"]
    print("Creating rating.csv to store data")
    with open(ratingcsv, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)



poslist = []
poslist2 = []
neglist = []
neglist2 = []

stops = set(stopwords.words("English"))
wordss = set(words.words())

with open(filename) as data_file:    
    data = json.loads(data_file.read())
    
    for x in range(len(data)): 
    
        reviewText = data[x]['text']
        stars = data[x]['stars']
        
        content = nltk.word_tokenize(reviewText)
        content = [w.lower() for w in content] #normalizing the text
        ps = nltk.PorterStemmer()
        content = set([ps.stem(w) for w in content if w in wordss and w not in stops]) 
        #filtering out stop words and dashes/ other symbols
        #turn into set to remove duplicate lemmas in the same review
        for word in content:
            if stars == 1: #creates a list of tuples, each tuple contains the lemma and star rating
                t = (word, stars)
                neglist.append(t)
            if stars == 5:
                t = (word, stars)
                poslist.append(t)
            
               
    neglist2 = [z for z in neglist if neglist.count(z) > 9] #removes any occurences less than 10
    poslist2 = [z for z in poslist if poslist.count(z) > 9]
    
    negcount = Counter(elem[0] for elem in neglist2) #counts the occurences of each word
    negsort = sorted(negcount.items(), key=lambda item: item[1])
    if len(negsort) > 500:
        neglength = len(negsort)
        fiveneg = negsort[neglength-500]
    else:
        fiveneg = negsort
    
    poscount = Counter(elem[0] for elem in poslist2)
    possort = sorted(poscount.items(), key=lambda item: item[1])
    if len(possort) > 500:
        poslength = len(possort)
        fivepos = possort[poslength-500]
    else:
        fivepos = possort
    for w in fiveneg: 
        row = [w[0], '1']
        with open(ratingcsv, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(row)   
    for w in fivepos: 
        row = [w[0], '5']
        with open(ratingcsv, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(row)          
 
##ls = nltk.LancasterStemmer()
##stops = set(nltk.corpus.stopwords.words("English"))
##result = [ls.stem(word.lower()) for word
##            in nltk.wordpunct_tokenize(text)
  ##          if word.isalpha()
    ##        and word not in stops]
 
