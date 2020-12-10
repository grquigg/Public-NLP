import json
import csv
import langdetect
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

from langdetect import detect, detect_langs


def deleteUntilSpace(string, substring):
	if string.find(substring) == -1:
		return string
	index = string.find(substring)
	counter = index + len(substring) #place the counter at the first character past the beginning of the array
	deleteString = substring

	while (counter < len(string) and string[counter] != ' '):
		deleteString = deleteString + string[counter]
		counter = counter + 1
	string = string.replace(deleteString, "")
	return string


tweets_per_country = []
user_ids_dictionary = {}
target_string = ""
headers = ["Country"]
deleteStrings = ["@", "#", "https"] #remove hashtags, retweets, links, etc
filename = './data/data2020-09-30.jsonl' 
#have to look through the tweets collected from September 30th as well because there are some tweets collected in this
# file that are marked as October 1st
with open(filename, "r", encoding='utf-8') as file:
    count = 0
    for line in file:
            try:
                parsed = json.loads(line)
                if(parsed["retweeted"] == False):
                    date = parsed["created_at"]
                    if(date[4:7] == "Oct"):
                        text = parsed["full_text"]
                        if(target_string in text or "symptoms" in text):
                            if(parsed["place"] != None):
                                country = parsed["place"]["country_code"]
                            else:
                                country = "UND"
                            
                            if(country not in user_ids_dictionary):
                                user_ids_dictionary[country] = {}

                            date_name = "10/1/2020"

                            if date_name not in headers:
                                headers.append(date_name)

                            if date_name not in user_ids_dictionary[country]:
                                user_ids_dictionary[country][date_name] = {}

                            user_id = parsed["user"]["id"]
                            if(user_id not in user_ids_dictionary[country][date_name]):
                                user_ids_dictionary[country][date_name][user_id] = []

                            for delStr in deleteStrings:
                                while (text.find(delStr) != -1):
                                    text = deleteUntilSpace(text, delStr)

                            text = text.lower()
                            tokenizer = nltk.RegexpTokenizer(r"\w+")
                            tokens = tokenizer.tokenize(text)
                            if(len(tokens) != 0): #if the number of tokens in the string is not 0
                                try:
                                    lang = detect(text)
                                except:
                                    print("Error")
                                    lang = parsed["lang"]
                                if lang not in user_ids_dictionary[country][date_name][user_id]:
                                    user_ids_dictionary[country][date_name][user_id].append(lang)
            except KeyError:
                continue
    print(count)
pathname = './data/data2020-10-'
for i in range(31):
    extension = str(i+1)
    if i+1 < 10:
        extension = '0' + str(i+1)
    filename = pathname + extension + '.jsonl'
    print(filename)
    with open(filename, "r", encoding='utf-8') as file:
        for line in file:
            try:
                parsed = json.loads(line)
                if(parsed["retweeted"] == False):
                    text = parsed["full_text"]
                    if(target_string in text or "symptoms" in text):
                        date = parsed["created_at"]
                        if(date[4:7] == "Oct"):
                            if(parsed["place"] != None):
                                country = parsed["place"]["country_code"]
                            else:
                                country = "UND"
                            
                            if(country not in user_ids_dictionary):
                                user_ids_dictionary[country] = {}
                            if (date[8] == '0'):
                                date_name = "10/" + date[9:10] + "/2020"
                            else:
                                date_name = "10/" + date[8:10] + "/2020"
                            
                            if date_name not in headers:
                                headers.append(date_name)

                            if date_name not in user_ids_dictionary[country]:
                                user_ids_dictionary[country][date_name] = {}

                            user_id = parsed["user"]["id"]
                            if(user_id not in user_ids_dictionary[country][date_name]):
                                user_ids_dictionary[country][date_name][user_id] = []

                            for delStr in deleteStrings:
                                while (text.find(delStr) != -1):
                                    text = deleteUntilSpace(text, delStr)
                            text = text.lower()
                            tokenizer = nltk.RegexpTokenizer(r"\w+")
                            tokens = tokenizer.tokenize(text)
                            if(len(tokens) != 0):
                                try:
                                    lang = detect(text)
                                except:
                                    print("Error")
                                    lang = parsed["lang"]
                                if lang not in user_ids_dictionary[country][date_name][user_id] and lang != "":
                                    user_ids_dictionary[country][date_name][user_id].append(lang)
            except KeyError:
                continue
print(headers)
covid_per_country = {}
WHO_data_file = "WHO-COVID-19-global-data.csv"
with open(WHO_data_file, "r") as covid_data:
    csv_reader = csv.DictReader(covid_data)
    for row in csv_reader:
        if (row["ï»¿Date"] != ""):
            date = row["ï»¿Date"]
            country = row["Country_code"]
            if country not in covid_per_country:
                covid_per_country[country] = {}
                covid_per_country[country]["Country"] = row["Country_code"]
            covid_per_country[country][date] = row["New_cases"]
        else:
            break

print(len(covid_per_country))
print(covid_per_country["US"])
totals_per_day = {}
totals_per_day["Country"] = "Total"
for country in user_ids_dictionary:
    array = {}
    array["Country"] = country

    for date in user_ids_dictionary[country]:
        array[date] = 0
        count = 0
        for user in user_ids_dictionary[country][date]:
            count+=1
        array[date] = count

        if date not in totals_per_day:
            totals_per_day[date] = 0
        totals_per_day[date] += array[date]
    tweets_per_country.append(array)

# for entry in tweets_per_country:
#     for date in entry:
#         if(date != "Country"):
#             entry[date] = entry[date] / totals_per_day[date]

csv_file = "octTwitter.csv"
with open(csv_file, "w") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writeheader()
    for entry in tweets_per_country:
        print(entry)
        writer.writerow(entry)
        if entry["Country"] in covid_per_country:
            print(covid_per_country[entry["Country"]])
            writer.writerow(covid_per_country[entry["Country"]])
        else:
            writer.writerow({})
    writer.writerow(totals_per_day)

    