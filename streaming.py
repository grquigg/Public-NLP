import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from datetime import datetime


##removed the tokens and consumer_secret and consumer_keys

today = datetime.date(datetime.now())
filename = "data" + str(today) + ".txt"
file = open(filename, "a", encoding="utf-8")
class StdOutListener(StreamListener):
	val = 0
	def on_data(self, data):
		if not (self.val >= 1000):
			tweet = json.loads(data)
			try:
				if(tweet["place"] != None):
					file.write(str(tweet["id"]) + "\n")
					self.val = self.val + 1
					return True
			except KeyError:
				pass
		else:
			return False

	def on_error(self, status):
		print(status)

if __name__ == '__main__':

	listener = StdOutListener()
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	stream = Stream(auth, listener, tweet_mode='extended')

	stream.filter(track=['coronavirus', 'covid-19', 'covid'])
