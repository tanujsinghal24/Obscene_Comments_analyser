#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 06:03:28 2019

@author: tanujsinghal
"""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import re
import copy
from sklearn.metrics import jaccard_similarity_score,confusion_matrix
from sklearn.externals import joblib
import os
import pathlib
import pickle

if __name__=='__main__':
        hin=pd.read_csv("Hinglish_Profanity_List.csv")
        train = pd.read_csv("train.csv")
        test = pd.read_csv("test.csv")
        columns = ['obscene','insult','toxic','severe_toxic','identity_hate','threat']
        hin_bad_words = hin.iloc[:,0].values.tolist()
        bad_words_to_english = hin.iloc[:,1].values.tolist()
        hin = hin.iloc[:,:-1].values.tolist()
        train, test = train_test_split(train, test_size=0.2)
        labels = train.iloc[:,2:]
        train_data = train.iloc[:,1]
        test_data = test.iloc[:,1]

        features = 5000
        ngram = (1,2)
        vectorizer = TfidfVectorizer(stop_words='english',\
                                token_pattern = "\w*[a-z]\w*",\
                                ngram_range=ngram,\
                                max_features=features)



        train_features = vectorizer.fit_transform(train_data)
        filename='vect'
        pickle.dump(vectorizer, open(filename, 'wb'))
        test_features = vectorizer.transform(test_data)
        logreg = LogisticRegression(C=10,solver="liblinear")
        models={}
        logistic_results = pd.DataFrame(columns=columns)    
        cnt=0
        
        for i in columns:
                y = train[i]
                models[i]=copy.copy(logreg.fit(train_features, y))
                filename = "model_"+ str(cnt)
                pickle.dump(models[i], open(filename, 'wb'))
                ypred_X = logreg.predict(train_features)
                testy_prob = logreg.predict_proba(test_features)[:,1]
                logistic_results[i] = testy_prob
                cnt+=1
def abusive_hinglish_to_english(data):
    hin=pd.read_csv("Hinglish_Profanity_List.csv")
    hin_bad_words = hin.iloc[:,0].values.tolist()
    bad_words_to_english = hin.iloc[:,1].values.tolist()
    hin = hin.iloc[:,:-1].values.tolist()
    cnt=0
    for sentence in data:
        wordList = sentence.split()
        for word in hin_bad_words:
            if word in wordList:
                x=wordList.index(word)
                wordList[x]=bad_words_to_english[hin_bad_words.index(word)]
        sentence = ' '.join(wordList)
        data[cnt]=sentence
        cnt+=1
    return data

def check_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    
def myinput(vectorizer,model,val):
    sent="Thank you for understanding. I think very highly of you and would not revert without discussion."
    sent2="Yo bitch Ja Rule is more succesful then you'll ever be whats up with you and hating you sad mofuckas...i should bitch slap ur pethedic white faces and get you to kiss my ass you guys sicken me. Ja rule is about pride in da music man. dont diss that shit on him. and nothin is wrong bein like tupac he was a brother too...fuckin white boys get things right next time.,"
    sen3="Explanation Why the edits made under my username Hardcore Metallica Fan were reverted? They weren't vandalisms, just closure on some GAs after I voted at New York Dolls FAC. And please don't remove the template from the talk page since I'm retired now.89.205.38.27"
    sen4="COCKSUCKER BEFORE YOU PISS AROUND ON MY WORK"
    sen5="While booking during rush hour, it is always advisable to check this box ON. It will deduct your FULL ticket amount first. After that it check whether confirmed ticket available or not. If confirmed ticket not available it will show ticket not available. Within 2 days will get your full amount Refund."
    sen6="madarchod chutia"
    sent7='F**K YOU!good day'
    l=[sent,sent2,sen3,sen4,sen5,sen6,sent7]
    l=abusive_hinglish_to_english(l)
    df = pd.DataFrame(l)
    user_data = vectorizer.transform(l)
    results2 = pd.DataFrame(columns=columns)
    for i in columns:
        user_results = models[i].predict_proba(user_data)[:,1]
        results2[i] = user_results
    y=results2.iloc[val].values
    x = columns
    plt.ylim(0, 100)
    plt.tight_layout()
    plt.bar(x, height= y)
    plt.show()
    plt.savefig('foo.png')
    return df,results2

def myinput_network(text):
    columns = ['obscene','insult','toxic','severe_toxic','identity_hate','threat']
    sent="Thank you for understanding. I think very highly of you and would not revert without discussion."
    sent2="Yo bitch Ja Rule is more succesful then you'll ever be whats up with you and hating you sad mofuckas...i should bitch slap ur pethedic white faces and get you to kiss my ass you guys sicken me. Ja rule is about pride in da music man. dont diss that shit on him. and nothin is wrong bein like tupac he was a brother too...fuckin white boys get things right next time.,"
    sen3="Explanation Why the edits made under my username Hardcore Metallica Fan were reverted? They weren't vandalisms, just closure on some GAs after I voted at New York Dolls FAC. And please don't remove the template from the talk page since I'm retired now.89.205.38.27"
    sen4="COCKSUCKER BEFORE YOU PISS AROUND ON MY WORK"
    sen5="While booking during rush hour, it is always advisable to check this box ON. It will deduct your FULL ticket amount first. After that it check whether confirmed ticket available or not. If confirmed ticket not available it will show ticket not available. Within 2 days will get your full amount Refund."
    sen6="madarchod chutia"
    sent7='F**K YOU!good day'
    l=[sent,sent2,sen3,sen4,sen5,sen6,sent7,text]
    l=[text,sent2]
    if len(text)>1 and type(text) is list:
            l=text
            res,x=myinput_network2(l)
            return res,x
    l=abusive_hinglish_to_english(l)
    df = pd.DataFrame(l)
    f='vect'
    vect= pickle.load(open(f, 'rb'))
    user_data = vect.transform(l)
    results2 = pd.DataFrame(columns=columns)
    cnt=0
    mymodels={}
    for i in range(6):
        filename='model_'+str(i)
        mymodels[columns[i]]= pickle.load(open(filename, 'rb'))
    for i in range(6):
        user_results = mymodels[columns[i]].predict_proba(user_data)[:,1]
        results2[columns[i]] = user_results
    x = columns
    return results2.iloc[0].values,x
def myinput_network2(text):
        columns = ['obscene','insult','toxic','severe_toxic','identity_hate','threat']
        x = columns
        if len(text)>1:
                l=text
                print(l)
                print(type(l))

        l=abusive_hinglish_to_english(l)
        df = pd.DataFrame(l)
        f='vect'
        vect= pickle.load(open(f, 'rb'))
        user_data = vect.transform(l)
        results2 = pd.DataFrame(columns=columns)
        cnt=0
        mymodels={}   
        filename='model_'+str(2)
        mymodels[columns[2]]= pickle.load(open(filename, 'rb'))
        user_results = mymodels[columns[2]].predict_proba(user_data)[:,1]
        results2[columns[2]] = user_results     
        return results2[columns[2]].values,x