import tweepy
import json
from tweepy import OAuthHandler
from win10toast import ToastNotifier
n = ToastNotifier()

consumer_key = 'lSC7SJ2ZN24Y9oYAog43cX628'
consumer_secret = 'AOwfcavm9A3r02O7fzuNuCrrqTlBh2YmGBDxdlZtHfJnVior9c'
access_token = '759544043361734656-whQmxqLWM5UUzkw0wkxkrwqS8iNJzXl'
access_token_secret = 'xeayYvSWfYQtoMEecN04a7INEUj5AQwqeH4k68OoVznPu'


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

