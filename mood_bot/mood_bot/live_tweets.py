from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
from nltk import sentiment_mod
import os



#consumer key, consumer secret, access token, access secret.
ckey = "GqrX1h40eg2mZNOiDC40lbwZj"
csecret = os.environ.GET('CON_SECRET')
atoken = "854074011231305728-rJolfVKlr5w7F8TaoYMct7ClxLjeC8G"
asecret = os.environ.GET('ACC_SECRET')


class listener(StreamListener):

    def on_data(self, data):

        all_data = json.loads(data)

        tweet = all_data["text"]
        sentiment_value, confidence = sentiment_mod.sentiment(tweet)
        print(tweet, sentiment_value, confidence)

        return True

    def on_error(self, status):
        print(status)


def text_stream(subject):
    """."""
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    twitter_stream = Stream(auth, listener())
    twitter_stream.filter(track=[subject])
