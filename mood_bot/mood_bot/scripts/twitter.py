import re
import os
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob


class TwitterRequest(object):
    """docstring for TwitterRequest"""
    def __init__(self):
        ckey = "GqrX1h40eg2mZNOiDC40lbwZj"
        csecret = os.environ['CON_SECRET']
        atoken = "854074011231305728-rJolfVKlr5w7F8TaoYMct7ClxLjeC8G"
        asecret = os.environ['ACC_SECRET']
        try:
            self.auth = OAuthHandler(ckey, csecret)
            self.auth.set_access_token(atoken, asecret)
            self.api = tweepy.API(self.auth)
        except:  # pragma no cover
            print('Error: Authentication failed')

    def tweet_prep(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w+:\/\/\S+)", " ", tweet).split())

    def tweet_sentiment(self, tweet):
        analysis = TextBlob(self.tweet_prep(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def tweet_grab(self, query, count):
        tweets = []
        try:
            tweets_fetched = self.api.search(q=query, count=count)

            for tweet in tweets_fetched:
                tweets_parsed = {}
                tweets_parsed['text'] = tweet.text
                tweets_parsed['sentiment'] = self.tweet_sentiment(tweet.text)

                if tweet.retweet_count > 0:
                    if tweets_parsed not in tweets:
                        tweets.append(tweets_parsed)
                else:
                    tweets.append(tweets_parsed)
            return tweets
        except tweepy.TweepError: # pragma no cover
            print('Error : ' + str(tweepy.TweepError))


def percentage(number):
        return ("%.2f" % (100 * number))


def main(query, count=100):
    results = []
    pos_list = []
    neg_list = []
    api = TwitterRequest()
    tweets = api.tweet_grab(query=query, count=count)

    pos_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    results.append(percentage((len(pos_tweets) / len(tweets))))
    neg_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    results.append(percentage((len(neg_tweets) / len(tweets))))
    results.append(percentage(((len(tweets) - len(neg_tweets) - len(pos_tweets))/len(tweets))))
    for tweet in pos_tweets[:5]:
        pos_list.append(tweet['text'])
    for tweet in neg_tweets[:5]:
        neg_list.append(tweet['text'])
    results.append(pos_list)
    results.append(neg_list)
    return results
