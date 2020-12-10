import json
import pandas as pd 
import operator
import csv
import os.path
from os import path

paths = ['data2020-09-16.txt']
date="9/16/2020"

tweets_data = []
for pathname in paths:
	tweets_file = open(pathname, "r", encoding="utf-8")
	for line in tweets_file:
		try:
			if(line != "\n"):
				tweet = json.loads(line)
				if (tweet["lang"] != ""):
					tweets_data.append(tweet)
		except json.JSONDecodeError:
			print("Syntax error")
		except:
			continue

print(len(tweets_data))
languages={}
for tweet in tweets_data:
	try:
		text = tweet['text'].lower()
		if(text.find("coronavirus") != -1 or text.find("covid") != -1):
			language = tweet['lang']
			#print(text)
			if language in languages:
 				languages[language] = languages[language] + 1
			else:
				languages[language] = 1
	except KeyError:
		continue

# sorted_tokens = dict(sorted(languages.items(), key=operator.itemgetter(1), reverse = True))
#print(sorted_tokens)

	#print(key, " ", value)

tweets = pd.DataFrame(tweets_data)
lang_list = dict(tweets.lang.value_counts())
#country_list = tweets.country.value_counts()
print(lang_list)
#print(country_list)
rows = []
existing_langs = []
fields = None
new_rows = []
with open("lang_data.csv", newline='') as lang_reader:
	reader = csv.DictReader(lang_reader)
	fields = reader.fieldnames
	for row in reader:
		existing_langs.append(row["Lang"])
		#print(row)
		rows.append(row)

	if fields == None:
		fields = ['Lang']

	if date not in fields:
		fields.append(date)
	print(fields)
	for row in rows:
		new_row = dict(row)
		print(new_row)
		if(new_row["Lang"] in lang_list):
			new_row[date] = lang_list[new_row["Lang"]]
		print(new_row)
		new_rows.append(new_row)

with open("lang_data.csv", "w", newline='') as lang:
	
	if fields == None:
		fields = ['Lang']

	if date not in fields:
		fields.append(date)

	for key, val in tweets.lang.value_counts().iteritems():
		if key not in existing_langs:
			entry = {}
			entry["Lang"] = key
			entry[date] = val
			print(entry)
			new_rows.append(entry)
	writer = csv.DictWriter(lang, fieldnames=fields)
	writer.writeheader()
	for row in new_rows:
		writer.writerow(row)

	