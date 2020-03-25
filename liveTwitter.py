import time
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
from textblob import TextBlob
import matplotlib.pyplot as plt
import re
import tokens
from new import myinput_network
ckey=tokens.consumer_key
csecret=tokens.consumer_secret
atoken=tokens.access_token
asecret=tokens.access_token_secret
filename = "./trained_models/toxic-text-analyser/tweetsa.txt"
#paths need to be rest

class listener(StreamListener):
    
    def on_data(self, data):
        all_data = json.loads(data)
        
        tweet = all_data["text"]
        vulgarity_value,x = myinput_network(tweet)
        print(tweet, vulgarity_value)
        
        return True

    def on_error(self, status):
        print(status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["fun"]) # Search for tweets having keyword "fun"