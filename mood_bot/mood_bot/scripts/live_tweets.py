from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import os


class Listener(StreamListener):
    def __init__(self):
        ckey = "GqrX1h40eg2mZNOiDC40lbwZj"
        csecret = os.environ['CON_SECRET']
        atoken = "854074011231305728-rJolfVKlr5w7F8TaoYMct7ClxLjeC8G"
        asecret = os.environ['ACC_SECRET']
        try:
            self.auth = OAuthHandler(ckey, csecret)
            self.auth.set_access_token(atoken, asecret)
            twitter_stream = Stream(auth=self.auth, listener=self)
            twitter_stream.filter(track=['Donald Trump'])
        except:
            print('Error: Authentication failed')

    def on_data(self, data):

        all_data = json.loads(data)

        tweet = all_data["text"]
        print(tweet)

        return True

    def on_error(self, status):
        print(status)


def main():
    """."""
    new_listener = Listener()
    return new_listener.on_data