#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 06:03:28 2019

@author: tanujsinghal
"""
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time
import json
import re
import pandas as pd
import numpy as np
from os.path import join, dirname, realpath
access_token = "1115607808185995264-em8QLLFJ6ESWiVRM5G77euAA0rmaxU"
access_token_secret = "pnfdtIsloJsg9huAUb8mVAMApYqv9fyiJRqdTaJwkYvS0"
consumer_key = "wM7VnB9KDsU1ZiezePZmyRSZo"
consumer_secret = "0Vd3EiWZQppmOTkd8s8lTynU1T9rBs5auMQQvJy9xNE1O49yXJ"
path= join(dirname(realpath(__file__)), '')
class StdOutListener(StreamListener):
    def __init__(self, time_limit=5):
        self.start_time = time.time()
        self.limit = time_limit
        self.saveFile = open(path+'tweetsfile.json', 'w')
        print(45)
    def on_data(self,data):
            if time.time() - self.start_time < self.limit:    
                self.saveFile.write(data)
                self.saveFile.write('\n')
            else:
                self.saveFile.close()
                return False
            return True
    def on_error(self, status):
        print(status)
def word_in_text(word, text):
    word = word.lower()
    text = text.lower()
    match = re.search(word, text)
    if match:
        return True
    return False
def preprocess_data():
    tweets_data = []
    tweets_file = open('tweetsfile.json', "r")
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweets_data.append(tweet)
        except:
            continue
    tweets = pd.DataFrame()
    tweets['text'] = list([tweet['text'] for tweet in tweets_data])
    tweets['lang'] = list([tweet['lang'] for tweet in tweets_data])
    tweets['fuck'] = tweets['text'].apply(lambda tweet: word_in_text('dumb', tweet))
    tweets['sex'] = tweets['text'].apply(lambda tweet: word_in_text('stupid', tweet))
    tweets['kill'] = tweets['text'].apply(lambda tweet: word_in_text('kill', tweet))
    tweets['bitch'] = tweets['text'].apply(lambda tweet: word_in_text('hell', tweet))
    tweets['hell'] = tweets['text'].apply(lambda tweet: word_in_text('shit', tweet))
    tweets['bad'] = tweets['text'].apply(lambda tweet: word_in_text('bad', tweet))
    tweets=tweets[((tweets['fuck'] == 1)|(tweets['bitch'] == 1)|(tweets['sex'] == 1)|(tweets['hell'] == 1)) & (tweets['lang'] == 'en')]
    tweets=tweets.iloc[:,0:2]
    tweetlist = tweets['text'].values.tolist()
    return tweetlist,tweets

def tweetsGenerator():
    l = StdOutListener()
    values=['dumb','stupid','kill','hell']
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.filter(track=values)
    tweetlist,df=preprocess_data()
    while len(df) < 5:
        tweetlist,df=tweetsGenerator()
    return tweetlist,df
if __name__ == '__main__':
    tweetlist,df=tweetsGenerator()
    while len(df) < 5:
        tweetlist,df=tweetsGenerator()