import tweepy
import json
from tweepy import OAuthHandler
from win10toast import ToastNotifier
n = ToastNotifier()


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

file = open("process.txt", "a", encoding = "utf-8")


count = 0
for status in tweepy.Cursor(api.home_timeline, tweet_mode='extended').items(10):
	json_str = json.dumps(status._json)
	parsed = json.loads(json_str)
	file.write(json.dumps(parsed, indent=4, sort_keys=True))
	file.write("\n")

n.show_toast("Tweepy", "Successfully recorded data", duration=5)

