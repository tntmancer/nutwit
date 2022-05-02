
from os import unlink
import unittest
from nutwit import Tweeter, load_secrets
import pickle
import json

# To run tests from the command line: 
# Enter anything other than 'run when prompted,
# then input  python -m unittest tests.py

class TweetMock:
    def __init__(self, text):
        self.text = text

class Test_Tweeter(unittest.TestCase):
    """Tests non-API based methods of Tweeter Class"""
    def setUp(self):
        secrets_file = "secrets.json"
        secrets = load_secrets(secrets_file)
        self.secrets = secrets
        self.tweeter = Tweeter(*secrets)

    def test_filter_empty(self):
        """Case where filter list = []"""
        tweet_list = [TweetMock("Admissions"), TweetMock("Giving Day")]
        filt_list = []
        x = self.tweeter.filter_tweet_list(tweet_list, filt_list)
        self.assertEqual(len(x), 2)

    def test_filter_tweets_empty(self):
        """Case where list of tweets = []"""
        tweet_list = []
        filt_list = ["Giving Day", "Admissions", "Illinois", "$"]
        x = self.tweeter.filter_tweet_list(tweet_list, filt_list)
        self.assertEqual([], x)

    def test_filter_none_pass(self):
        """Case where both lists are nonempty, but filters all tweets"""
        tweet_list = [TweetMock("Admissions"), TweetMock("Giving Day")]
        filt_list = ["Giving Day", "Admissions", "Illinois", "$"]
        x = self.tweeter.filter_tweet_list(tweet_list, filt_list)
        self.assertEqual([], x)

    def test_filter_some_pass(self):
        """Case where both lists are nonempty, but only some tweets filtered"""
        tweet_list = [TweetMock("good"), TweetMock("Giving Day")]
        filt_list = ["Giving Day", "Admissions", "Illinois", "$"]
        x = self.tweeter.filter_tweet_list(tweet_list, filt_list)
        self.assertEqual(len(x), 1)
        self.assertEqual(x[0].text, "good")

    def test_load_dict_dne(self):
        """dictionary pickle does not exist"""
        file_name = "dne.py"
        self.tweeter.load_dictionary_from_file(file_name)
        self.assertEqual({}, self.tweeter.dict)

    def test_load_dict_complete(self):
        """dictionary pickle valid"""
        dict = {"timeline": 0}
        pickle_file = "valid.pkl"
        with open(pickle_file, 'wb') as f:
            pickle.dump(dict, f)
        self.tweeter.load_dictionary_from_file(pickle_file)
        unlink(pickle_file)
        self.assertEqual(dict, self.tweeter.dict)

    def test_save_dict(self):
        """file does exist"""
        self.tweeter.dict = {"Is This It": "Someday"}
        pickle_file = "saved.pkl"
        self.tweeter.save_dictionary_to_file(pickle_file)
        with open(pickle_file, 'rb') as f:
            dict = pickle.load(f)
        unlink(pickle_file)
        self.assertEqual(dict, self.tweeter.dict)
        
    def test_load_secrets_dne(self):
        """file does not exist"""
        file_name = "dne.py"
        with self.assertRaises(FileNotFoundError):
            secrets = load_secrets("dne.py")

    def test_load_secrets_complete(self):
        """File has required fields"""
        data = ["a", "b", "c", "d", "e"]
        secret_file = "complete.json"
        with open(secret_file, 'w') as f:
            json.dump(data, f)
        data_from_file = load_secrets(secret_file)
        unlink(secret_file)
        self.assertEqual(data, data_from_file)
    
