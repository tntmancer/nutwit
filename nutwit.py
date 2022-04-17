import tweepy
import pickle
import json
 
class Tweeter:
    def __init__(self, api_key, api_key_secret, bearer_token, token, token_secret, last_seen_dict = None):
        if last_seen_dict == None:
            self.dict = {}
            self.dict["timeline"] = 0
            self.dict["#Northeastern"] = 0
            self.dict["HowlinHuskies"] = 0
            self.dict["LikeAHusky"] = 0
           
        else:
            self.dict =  last_seen_dict
 
        auth = tweepy.OAuth1UserHandler(api_key, api_key_secret)
        auth.set_access_token(token, token_secret)
        #self.client = tweepy.Client(bearer_token, wait_on_rate_limit=True)
        #auth = tweepy.OAuth2BearerHandler(bearer_token)
        api = tweepy.API(auth, wait_on_rate_limit=True)
        self.api = api
 
    def get_timeline(self):
        """Gets 200 tweets from account timeline, saves most recent to dict, returns list of unseen tweets
        tweet ids are time ordered, uses this to see if tweet was in previous batch"""
        timeline_tweets = tweepy.Cursor(self.api.home_timeline, count=2).items(100) #gets as many tweets from timeline as possible (100)
        unseen = []
        max = 0
        for tweet in timeline_tweets:
            if tweet.id > self.dict["timeline"]:
                unseen.append(tweet)
                if tweet.id > max:
                    max = tweet.id
        self.dict["timeline"] = max
        return unseen
   
    def get_Northeastern(self):
        list_Northeastern = []
        max = 0
        for tweet in self.api.search(q="#Northeastern", lang="en", rpp=100):
            if tweet.id > self.dict["#Northeastern"]:
                list_Northeastern.append(tweet)
                if tweet.id > max:
                    max = tweet.id
        if max > self.dict["#Northeastern"]: self.dict["#Northeastern"] = max
        return list_Northeastern
   
    def get_HowlinHuskies(self):
        list_HowlinHuskies = []
        max = 0
        for tweet in self.api.search(q="HowlinHuskies", lang="en", rpp=100):
            if tweet.id > self.dict["HowlinHuskies"]:
                list_HowlinHuskies.append(tweet)
                if tweet.id > max:
                    max = tweet.id
        if max > self.dict["#HowlinHuskies"]: self.dict["#HowlinHuskies"] = max
        return list_HowlinHuskies
   
    def get_LikeAHusky(self):
        list_LikeAHusky = []
        max = 0
        for tweet in self.api.search(q="LikeAHusky", lang="en", rpp=100):
            if tweet.id > self.dict["LikeAHusky"]:
                list_LikeAHusky.append(tweet)
                if tweet.id > max:
                    max = tweet.id
        if max > self.dict["LikeAHusky"]: self.dict["#LikeAHusky"] = max
        return list_LikeAHusky
   
    def process_tweet_list(self, tweet_list):
        for tweet in tweet_list:
            print(f"{tweet.id} {tweet.text}")
            if ((tweet.in_reply_to_status_id is None) and not (tweet.user.id == "fan_neu") and not tweet.retweeted):
                print("retweeting")
                self.api.retweet(tweet.id)
   
    def save_to_file(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)


def load_secrets(filename):
    f = open(filename, "r")
    return json.load(f)

secrets = load_secrets("secrets.json")

bot = Tweeter(*secrets)
tl = bot.get_timeline()
# print(tl)
bot.process_tweet_list(tl)