# nutwit
This project is a twitter bot engineered to tweet out a cohesive feed relevant to Northeastern Undergraduates.
However, it can easily be tailored to create a feed for any reason or organization by changing what it follows,
the filters it uses, and the searches it operates on.

The Nutwit file is a class that connects to the twitter api with methods to search for specific topics,
pull from a timeline, and retweet a list of tweets.

Recently seen tweets are stored in a pickle, while the API tokens and keys are hidden from being leaked in a json file.

It also includes a function to run and constantly pull and process tweets, waiting after each run. It saves and loads
the most recently seen tweets to a pickle after each run.

The testing file includes tests with mock classes to make sure that the main methods of the Tweeter class function
as expected.
