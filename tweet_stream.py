"""
Example Stream listener for twitter API.

# Create App: apps.twtiter.com
# API Documentation: https://dev.twitter.com/overview/documentation
"""

import tweepy
import time
import cnfg
import json
from pymongo import MongoClient

class TweetListener(tweepy.StreamListener):

    def on_error(self, error_msg):
        print('Error: {}'.format(error_msg))

    def on_timeout(self):
        print('Timed Out.  Might be rate-limited.  Introduce Delay in the process.  ')
        time.sleep(10)

    def on_data(self, data):
        """This will be called each time we receive stream data"""
        client = MongoClient()

        # Use tweetdb database
        db = client.tweetdb

        # Decode JSON
        try:
            datajson = json.loads(data)

            # We only want to store tweets in English
            if "lang" in datajson and datajson["lang"] == "en":
                # Store tweet info into the cooltweets collection.
                db.tweetdb.insert(datajson)
        except Exception:
            print("Error in parsing data {}".format(data))

#For macbook
config = cnfg.load("/Users/bholligan/.ssh/.twitter_config")

auth = tweepy.OAuthHandler(config["consumer_key"],
                           config["consumer_secret"])
auth.set_access_token(config["access_token"],
                      config["access_token_secret"])


tweet_listener = TweetListener()
tweet_stream = tweepy.Stream(auth = auth, listener=tweet_listener)

tweet_stream.filter(track=['#rio2016', "#olympics", '#RioOlympics2016', 'olympics',
                            '#nbcolympics', '#bbcolympics', 'rio olympics'])
