import tweepy
 
class Tweeter:
    def __init__(self, api_key, api_key_secret, bearer_token, secret_token, last_seen_dict = None):
        if last_seen_dict == None:
            self.dict = {}
            self.dict["timeline"] = 0
           
        else:
            self.dict =  last_seen_dict
 
        auth = tweepy.OAuthHandler(api_key, api_key_secret)
        auth.set_access_token(bearer_token, secret_token)
        api = tweepy.API(auth, wait_on_rate_limit=True)
        self.api = api
 
    def get_timeline(self):
        """Gets 200 tweets from account timeline, saves most recent to dict, returns list of unseen tweets
        tweet ids are time ordered, uses this to see if tweet was in previous batch"""
        timeline_tweets = tweepy.Cursor(self.api.home_timeline).items(100) #gets as many tweets from timeline as possible (200)
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
            if ((tweet.in_reply_to_status_id is not None) or (tweet.user.id == self.me.id)) and not tweet.retweeted:
                tweet.retweet()

