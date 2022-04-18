from cgitb import text
from os import unlink
import unittest
from nutwit import Tweeter, load_secrets
import pickle

class TweetMock:
    def __init__(self, text):
        self.text = text

class Test_Tweeter(unittest.TestCase):
    """Tests non-API based methods of Tweeter Class"""
    def setUp(self):
        secrets_file = "secrets.json"
        secrets = load_secrets(secrets_file)

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
        
    def test_load_secrets_dne(self):
        """file does not exist"""
        file_name = "dne.py"
        with self.assertRaises(FileNotFoundError):
            secrets = load_secrets("dne.py")

    def test_load_secrets_incomplete(self):
        """file missing fields"""

    def test_load_secrets_complete(self):
        """File has required fields"""

    def test_save_dne(self):
        """file does not exist"""

    def test_save_exists(self):
        """file does exist"""