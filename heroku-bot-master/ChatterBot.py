# Dependencies
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
import tweepy
import json
import pandas as pd
import numpy as np
import random
import pylab
import requests
from pprint import pprint
import seaborn as sns
import time
from os import environ
from config import consumer_key, consumer_secret, access_token, access_token_secret
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

# consumer_key = environ["consumer_key"]
# consumer_secret = environ["consumer_secret"]
# access_token = environ["access_token"]
# access_token_secret = environ["access_token_secret"]

# Setup Tweepy API Authentication


def reply():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

    reply_tweet = api.user_timeline("@LJThompson15")
    recent_tweet = api.mentions_timeline(count = 1)
    reply_tweet_id = reply_tweet[0]["id"]
    recent_tweet_id = recent_tweet[0]["id"]
    recent_tweeter = recent_tweet[0]["user"]["screen_name"]
    compound_list = []
    positive_list = []
    negative_list = []
    neutral_list = []
    tweets_ago = []
    sentiment = {}
    counter = 0
    #if 2 > 1:
    if recent_tweet_id > reply_tweet_id:
        recent_tweet_text = recent_tweet[0]["text"]
        recent_tweet_text_split = recent_tweet_text.split()

        for x in range(len(recent_tweet_text_split)):
            if recent_tweet_text_split[x] == "analyze:":
                target_user = recent_tweet_text_split[int(x + 1)] 
                
                public_tweets = api.search(target_user, count = 100, result_type = "recent", pages = 1)
                
                for tweet in public_tweets["statuses"]:
                    results = analyzer.polarity_scores(tweet['text'])
                    compound_list.append(results["compound"])
                    positive_list.append(results["pos"])
                    neutral_list.append(results["neu"])
                    negative_list.append(results["neg"])
                    tweets_ago.append(counter)

                    sentiment.update({'Average Compound': compound_list,
                                    'Average Positive': positive_list,
                                    'Average Negative': negative_list,
                                    'Average Neutral': neutral_list})
                        
                    counter += 1

                
                
                sentiment_df = pd.DataFrame(sentiment)
                sentiment_df["tweets ago"] = tweets_ago
                y_vals = sentiment_df['Average Compound']
                x_vals = sentiment_df['tweets ago']
                plt.scatter(x_vals,y_vals)
                plt.title(f"{target_user}'s Compound Sentiment Score Recent Tweets")
                plt.xlabel("Recent 100 Tweets")
                plt.ylabel("Compound Sentiment Score")
                plt.savefig("resultplot")
                api.update_with_media ("resultplot.png",f"{target_user}'s sentiment analasys requested by @{recent_tweeter}'")
                pprint ("working")
    else:
        time.sleep(60)   
        pprint("sleeping")
while True:
    reply()