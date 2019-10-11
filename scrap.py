import pandas as pd
import tweepy
import csv
import json
import re
import time


class Tweet(object):
    def __init__(self):
        self.author_name = ''
        self.handle = ''
        self.tweet_content = ''
        self.likes = -1
        self.retweets = -1
        self.created_at = None

    def parse_text(self, text, additional=None):
        text = text[:text.rfind('http')]
        self.tweet_content = text
        if additional is not None:
            additional = '<Q> ' + \
                additional[:additional.rfind('http')] + ' </Q>'
            self.tweet_content = self.tweet_content + additional

    def __repr__(self):
        return {'author_name': self.author_name, 'handle': self.handle, 'tweet_content': self.tweet_content, 'likes': self.likes, 'retweets': self.retweets, 'created_at': self.created_at}

    def __str__(self):
        return 'author_name: ' + self.author_name + ' -- handle: ' + self.handle + ' -- tweet_content: \n' + self.tweet_content + '\n likes: ' + str(self.likes) + ' -- retweets: ' + str(self.retweets) + ' -- created_at: ' + str(self.created_at)


def parse_tweet(tweet_obj, api, accounts):
    try:
        tweet = Tweet()
        if(tweet_obj.full_text[:2] == 'RT'):
            retweeted = tweet_obj.retweeted_status
            if retweeted.user.screen_name in accounts:
                return None
            tweet = parse_tweet(retweeted, api, accounts)
        elif(tweet_obj.is_quote_status):
            r_tweet = api.get_status(
                tweet_obj.quoted_status_id, tweet_mode='extended')
            if(r_tweet.in_reply_to_status_id is not None):
                r_tweet.full_text = r_tweet.full_text[r_tweet.full_text.find(
                    '-') + 2:]
            tweet.author_name = tweet_obj.user.name
            tweet.handle = tweet_obj.user.screen_name
            tweet.parse_text(tweet_obj.full_text, additional=r_tweet.full_text)
            tweet.likes = tweet_obj.favorite_count
            tweet.retweets = tweet_obj.retweet_count
            tweet.created_at = tweet_obj.created_at

        else:
            tweet.author_name = tweet_obj.user.name
            tweet.handle = tweet_obj.user.screen_name
            tweet.parse_text(tweet_obj.full_text)
            tweet.likes = tweet_obj.favorite_count
            tweet.retweets = tweet_obj.retweet_count
            tweet.created_at = tweet_obj.created_at
        return tweet
    except:
        return None


def fetch_all_tweets(screen_name, api, accounts):
    all_objects = []
    # make initial request for most recent tweets (200 is the maximum allowed count)
    try:
        try:
            new_tweets = api.user_timeline(
                screen_name=screen_name, count=200, tweet_mode='extended')
        except tweepy.error.RateLimitError:
            time.sleep(15*60)
            new_tweets = api.user_timeline(
                screen_name=screen_name, count=200, tweet_mode='extended')
        # save the id of the oldest tweet less one
        oldest = new_tweets[-1].id - 1
        for tweet in new_tweets:
            if(tweet.in_reply_to_status_id is None):
                tweet_obj = parse_tweet(tweet, api, accounts)
                if tweet_obj is not None:
                    all_objects.append(tweet_obj)
            while len(new_tweets) > 0:
                try:
                    print("getting tweets before %s" % (oldest))
                    # all subsiquent requests use the max_id param to prevent duplicates
                    new_tweets = api.user_timeline(
                        screen_name=screen_name, count=200, max_id=oldest, tweet_mode='extended')
                    # update the id of the oldest tweet less one
                    if len(new_tweets) == 0:
                        break
                    oldest = new_tweets[-1].id - 1
                    for tweet in new_tweets:
                        if(tweet.in_reply_to_status_id is None):
                            tweet_obj = parse_tweet(tweet, api, accounts)
                            if tweet_obj is not None:
                                all_objects.append(tweet_obj)
                    print("...%s tweets downloaded so far" %
                          (len(all_objects)))
                except tweepy.error.RateLimitError:
                    time.sleep(15*60)
                    continue
    except tweepy.error.TweepError:
        pass
    return all_objects


def main():
    with open('cred.json') as json_file:
        data = json.load(json_file)

    # Twitter API credentials
    consumer_key = data['consumer_key']
    consumer_secret = data['consumer_secret']
    access_key = data['access_key']
    access_secret = data['access_secret']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    # accounts=['naval','Via_Benjamin','RortyWitt','EdLatimore','StoopToRise','AymPlanet','Wealth_Theory','alanhliang','TradingNirvana','modestproposal1','razyPolymath','SentientBonobo','webdevMason','stoic_dilettant','AJA_Cortes','martyrmade','PresentWitness_','millstoic','z3nblack','TheChuChu_','orangebook_','yawyr_vk','Noahpinion','ThomasSowell','LifeMathMoney','DejaRu22','lawsofaurelius','48_quotes','shl','cryptoseneca','paulg','TheCreativeFury','Kpaxs','TheAncientSage','DeeperThrill','mmay3r','DrRalphNap','TheStoicEmperor','uncannyinsights']
    accounts = ['naval']
    all_tweets = []
    for account in accounts:
        all_tweets += fetch_all_tweets(account, api)
    df = pd.DataFrame.from_records([s.__repr__() for s in all_tweets])
    df.to_csv('./tweets.csv', index=False)


if __name__ == "__main__":
    main()
    pass
