#!/usr/bin/python

import json
import pickle
#import sys
import time
import tweepy

class Tweeter:
    """Keeps track of most recent tweets from each search term in dictionary.
       Uses authentication tokens and api keys to create object that can access
       Twitter using the tweepy library. Methods included for saving object via 
       pickle, pulling tweets from timeline, and searching."""
    def __init__(self, api_key, api_key_secret, bearer_token, token, token_secret, last_seen_dict = None):
        """Initializes instance of tweeter class and connects to API. Saves most recent tweets to dictionary."""
        if last_seen_dict == None:
            self.dict = {}
            
        else:
            self.dict =  last_seen_dict
        auth = tweepy.OAuth1UserHandler(api_key, api_key_secret)
        auth.set_access_token(token, token_secret)
        #self.client = tweepy.Client(bearer_token, wait_on_rate_limit=True)
        #auth = tweepy.OAuth2BearerHandler(bearer_token)
        api = tweepy.API(auth, wait_on_rate_limit=True)
        self.api = api

    def __handle_new_tweets(self, search, raw_tweets):
        """The common code to process the tweet list and update the latest tweet id for the search."""
        tweets = []
        if not search in self.dict:
            self.dict[search] = 0

        print(f"+ Handling '{search}', got {len(raw_tweets)} tweets since {self.dict[search]}")
        for tweet in reversed(raw_tweets):
            if tweet.id > self.dict[search]:
                tweets.append(tweet)
                self.dict[search] = tweet.id
            else:
                print(f" - Skipped {tweet.id}: {tweet.text[0:50]}...")
        return tweets

    def search_tweets(self, search):
        """Generalized version of below searches. Takes a phrase to search, and pulls tweet from that search
        that have been tweeted since the last search. Saves most recently processed tweet to dictionary

        If the search phrase is 'timeline' it instead searches the user's timeline."""
        #Interacts w/ API, not testing using module
        since = self.dict.get(search) #[key] fails if key is non-existent, get() returns None
        count = 10

        if search == "timeline":
            tweets = self.api.home_timeline(count=count, since_id=since)
        else:
            tweets = self.api.search_tweets(q=search, lang="en", count=count, since_id=since)

        return self.__handle_new_tweets(search, tweets)
    
    def process_tweet_list(self, tweet_list):
        """Retweets all un-retweeted tweets from given list. Designed to process results from get_timeline
        and get_from_search"""
        #Interacts w/ API, not testing using module
        for tweet in tweet_list:
            if ((tweet.in_reply_to_status_id is None) and not (tweet.user.id == "fan_neu") and not tweet.retweeted):
                print(f" + Retweeting {tweet.id}: {tweet.text[0:50]}...")
                try:
                    tweet.retweet()
                except tweepy.errors.Forbidden:
                    print("    Already Retweeted!")
                #self.api.retweet(tweet.id)

    def filter_tweet_list(self, tweet_list, filter):
        """Filters out tweets that include certain phrases, such as "Giving Day" or "Admissions" or "$"
           that may not be of interest to current students (who don't have much money)"""
        filtered = []
        for tweet in tweet_list:
            good = True
            for word in filter:
                if tweet.text.find(word) != -1:
                    good = False
                    break
            if good:
                filtered.append(tweet)
        return filtered

    def save_dictionary_to_file(self, filename):
        """Loads dictionary to pickle. Using this to keep most recent tweets from each search inbetween runs of the program
           since it will be running on a server and methods depend on most recent tweets processed. Only doing dictionary so
           that the dictionary can be directly imported from a file to an existing object, since only the dictionary will
           change with each run."""
        # You can read the file for testing with: python -m pickle bot_state.pkl
        with open(filename, 'wb') as f:
            pickle.dump(self.dict, f)

    def load_dictionary_from_file(self, filename):
        """Loads dictionary from pickle Using this to keep most recent tweets from each search inbetween runs of the program
           since it will be running on a server and methods depend on most recent tweets processed. Only doing dictionary so
           that the dictionary can be directly imported from a file to an existing object, since only the dictionary will
           change with each run."""
        try:
            with open(filename, 'rb') as f:
                self.dict = pickle.load(f)
        except:
            self.dict = {}
    def main(self,
            state_file = "bot_state.pkl", 
            search_list = ["timeline", "#Northeastern", "HowlinHuskies", "LikeAHusky"], 
            filter = ["Giving Day", "$", "Admissions", "Illinois"], 
            delay_secs = 1 * 60):
        """Runs loop on given search terms, retweeting unseen tweets since past loop
        and filtering those including terms from the given list of filters. 
        Delays one minute between passes."""
        while True:
            print("Running searches:")
            self.load_dictionary_from_file(state_file)
            for search in search_list:
                self.process_tweet_list(self.filter_tweet_list(self.search_tweets(search), filter))
            self.save_dictionary_to_file(state_file)

            print(f"Sleeping for {delay_secs}s.  ZZZ zzz ...\n")
            time.sleep(delay_secs)

def load_secrets(filename):
    """Loads secrets from the given file (in json format so we can edit them).
    This is a separate file so we don't leak our secret tokens on github."""
    f = open(filename, "r")
    secrets = json.load(f)
    f.close()
    return secrets

secrets_file = "secrets.json"
secrets = load_secrets(secrets_file)
bot = Tweeter(*secrets)
bot.main()

#def main():
#    """Encapsulated in function so that file can be imported into testing 
#       file and the program body won't run."""
#    secrets_file = "secrets.json"
#    state_file = "bot_state.pkl"
#    search_list = ["timeline", "#Northeastern", "HowlinHuskies", "LikeAHusky"]
#    filter = ["Giving Day", "$", "Admissions", "Illinois"]
#    delay_secs = 1 * 60    # 1 minute
#
#    secrets = load_secrets(secrets_file)
#
#    bot = Tweeter(*secrets)
#
#
#    while True:
#        print("Running searches:")
#        bot.load_dictionary_from_file(state_file)
#        for search in search_list:
#            bot.process_tweet_list(bot.filter_tweet_list(bot.search_tweets(search), filter))
#        bot.save_dictionary_to_file(state_file)
#
#        print(f"Sleeping for {delay_secs}s.  ZZZ zzz ...\n")
#        time.sleep(delay_secs)

#if __name__ == "__main__":
#    main()
