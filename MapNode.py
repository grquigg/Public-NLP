import nltk
import json
import random
import langdetect

from langdetect import detect, detect_langs

class MapNode:
	def __init__(self, token, lang):
		self.token = token
		self.next = {}
		self.lang = lang

	def append_next(self, token, lang):
		if token in self.next and lang in self.next[token]:
			self.next[token][lang]["num"] = self.next[token][lang]["num"] + 1
			self.next[token]["total"] = self.next[token]["total"] + 1
		elif token in self.next:
			self.next[token][lang] = {}
			self.next[token][lang]["weight"] = 0.1
			self.next[token][lang]["num"] = 1
			self.next[token]["total"] = self.next[token]["total"] + 1
		else:
			self.next[token] = {}
			self.next[token][lang] = {}
			self.next[token][lang]["weight"] = 0.1
			self.next[token][lang]["num"] = 1
			self.next[token]["total"] = 1
		
	def toString(self):
		string = {
			'token': self.token,
			'lang': self.lang,
			'next': self.next
		}
		return string
token_list = {} #this is the association between the token and its corresponding map node
node_list = [] #this is simply the list of all the nodes 



def convertToString():
	string = {}
	for token, value in token_list.items():
		string[token] = token_list[token].toString()
	return string

model = open("model3.json", "a", encoding="utf-8")

def printModel():
	model.write(json.dumps(convertToString()))

def writeExampleModelToFile():
	deleteStrings = ["@", "#", "https"]
	tweets = [
		{
			"lang": "A",
			"text": "This is language A"
		},
		{
			"lang": "B",
			"text": "This is language B"
		},
		{
			"lang": "A",
			"text": "This is not language B"
		}
	]
	for tweet in tweets:
		print(tweet)
		# if (tweet["extended_tweet"]["full_text"] != ""):
		# 	text = tweet["extended_tweet"]["full_text"]
		# else:
		text = tweet["text"]
		for delStr in deleteStrings:
			while (text.find(delStr) != -1):
				text = deleteUntilSpace(text, delStr)
		text = text.lower()
		tokenizer = nltk.RegexpTokenizer(r"\w+")
		tokens = tokenizer.tokenize(text)
		#finally we can delete the first token if it is 'RT'
		if (len(tokens) != 0 and tokens[0] == "rt"):
			tokens.pop(0)

		if(len(tokens) != 0):
			start = "<s>"
			if start not in token_list:
				startNode = MapNode(start, "UNI")
				node_list.append(startNode)
				token_list[start] = startNode
			token_list[start].append_next(tokens[0], tweet["lang"])
			for i in range(1, len(tokens)):
				if tokens[i-1] not in token_list:
					name = MapNode(tokens[i-1], tweet["lang"])
					token_list[tokens[i-1]] = name
					node_list.append(name)
					
				token_list[tokens[i-1]].append_next(tokens[i], tweet["lang"])


			end = "</s>"
			if tokens[len(tokens)-1] not in token_list:
				endNode = MapNode(tokens[len(tokens)-1], "UNI")
				token_list[tokens[len(tokens)-1]] = endNode
				node_list.append(endNode)
			token_list[tokens[len(tokens)-1]].append_next(end, "UNI")
	printModel()

deleteStrings = ["@", "#", "https"]

def writeModelToFile():
	tweets_file = open("data6-8.txt", "r", encoding="utf-8")
	tweets = []
	for tweet in tweets_file:
		if(tweet != "\n"):
			try:
				tweets.index(tweet)
			except ValueError:
				tweets.append(tweet)

	for tweet in tweets:
		tweet = json.loads(tweet)
		try:
			if "extended_tweet" in tweet and "full_text" in tweet["extended_tweet"]:
				text = tweet["extended_tweet"]["full_text"]
			elif "text" in tweet:
				text = tweet["text"]
			else:
				text = ""
			for delStr in deleteStrings:
				while (text.find(delStr) != -1):
					text = deleteUntilSpace(text, delStr)
			text = text.lower()
			tokenizer = nltk.RegexpTokenizer(r"\w+")
			tokens = tokenizer.tokenize(text)
			#finally we can delete the first token if it is 'RT'
			if (len(tokens) != 0 and tokens[0] == "rt"):
				tokens.pop(0)
			try:
				lang = detect(text)
			except:
				if "lang" in tweet:
					lang = tweet["lang"]
				else:
					print("nothing")
					continue
			

			if(len(tokens) != 0):
				start = "<s>"
				if start not in token_list:
					startNode = MapNode(start, "UNI")
					node_list.append(startNode)
					token_list[start] = startNode
				token_list[start].append_next(tokens[0], lang)
				for i in range(1, len(tokens)):
					if tokens[i-1] not in token_list:
						name = MapNode(tokens[i-1], lang)
						token_list[tokens[i-1]] = name
						node_list.append(name)
					
					token_list[tokens[i-1]].append_next(tokens[i], lang)


				end = "</s>"
				if tokens[len(tokens)-1] not in token_list:
					endNode = MapNode(tokens[len(tokens)-1], "UNI")
					token_list[tokens[len(tokens)-1]] = endNode
					node_list.append(endNode)
				token_list[tokens[len(tokens)-1]].append_next(end, "UNI")
		except KeyError as k:
			raise k
	printModel()

def deleteUntilSpace(string, substring):
	if string.find(substring) == -1:
		return string
	index = string.find(substring)
	counter = index + len(substring) #place the counter at the first character past the beginning of the array
	deleteString = substring
	#print(len(string))
	while (counter < len(string) and string[counter] != ' '): #be aware of short circuiting here
		deleteString = deleteString + string[counter]
		counter = counter + 1
	string = string.replace(deleteString, "")
	return string

def getMapNodesForLanguage(lang):
	for node in node_list:
		for token in node.next:
			if lang in node.next[token] or (node.lang == lang and "UNI" in node.next[token]):
				file.write("Base token ")
				file.write(node.token)
				file.write(" Next token ")
				file.write(token)
				file.write("\n")
				#print(node.next[token])

def readModelFromFile():
	with open("model3.json", "r", encoding="utf-8") as modelFile:
		for line in modelFile:
			model = json.loads(line)
			for key, value in model.items():
				temp = MapNode(key, value["lang"])
				temp.next = value["next"]
				token_list[key] = temp
				node_list.append(temp)

def appendToModel(string, lang):
	string = string.lower()
	tokenizer = nltk.RegexpTokenizer(r"\w+")
	tokens = tokenizer.tokenize(string)

	if tokens[0] in token_list["<s>"].next:
		if lang in token_list["<s>"].next[tokens[0]]:
			token_list["<s>"].next[tokens[0]][lang]["num"] = token_list["<s>"].next[tokens[0]][lang]["num"] + 1
			token_list["<s>"].next[tokens[0]]["total"] = token_list["<s>"].next[tokens[0]]["total"] + 1
		else:
			token_list["<s>"].append_next(tokens[0], lang)
	else:
		token_list["<s>"].append_next(tokens[0], lang)

	for i in range(1, len(tokens)):
		if tokens[i-1] in token_list: 
			if tokens[i] in token_list[tokens[i-1]].next:
				if lang in token_list[tokens[i-1]].next[tokens[i]]:
					token_list[tokens[i-1]].next[tokens[i]][lang]["num"] = token_list[tokens[i-1]].next[tokens[i]][lang]["num"] + 1
					token_list[tokens[i-1]].next[tokens[i]]["total"] = token_list[tokens[i-1]].next[tokens[i]]["total"] + 1
				else:
					token_list[tokens[i-1]].append_next(tokens[i], lang)
			else:
				token_list[tokens[i-1]].append_next(tokens[i], lang)
		else:
			name = MapNode(tokens[i-1], tweet["lang"])
			token_list[tokens[i-1]] = name
			node_list.append(name)
	end = "</s>"
	if tokens[len(tokens)-1] in token_list:
		token_list[tokens[len(tokens)-1]].append_next(end, "UNI")
	

def getMapNode(token):
	if token in token_list:
		return token_list[token].next
	return None

# writeModelToFile()
readModelFromFile()
#machine learning algorithm
testing = []
with open("./data/data2020-10-01.jsonl", "r", encoding="utf-8") as json_file:
	for line in json_file:
		try:
			tweet = json.loads(line)
			testing.append(tweet)
		except:
			continue

# Normalize by the length of the sentence and also normalize these costs
learning_rate = 0.01
costs_per_epoch = {}
for j in range(100):
	print("Epoch " + str(j+1))
	costs = {}
	predictions = []
	net_cost = 0
	vector_cost = 0
	#1407 through 1408
	num_correct = 0
	total_num = 0
	percent = 0
	for tweet in testing[58:59]:
		try:
			string = tweet["full_text"]
			string = string.lower()
			for delStr in deleteStrings:
				while (string.find(delStr) != -1):
					string = deleteUntilSpace(string, delStr)
			tokenizer = nltk.RegexpTokenizer(r"\w+")
			tokens = tokenizer.tokenize(string)
			prediction = {}
			temp_costs = {}
			prediction["langs"] = {}
			prediction["totals"] = {}
			prediction["output"] = ""
			prediction["max"] = 0
			prediction["net_cost"] = 0
			try:
				lang = detect(string)
			except:
				print("Error")
				if "lang" in tweet:
					lang = tweet["lang"]
				else:
					print("nothing")
					continue
			if len(tokens) != 0:
				total_num+=1
				if(j == 0):
					appendToModel(string, lang)

				if tokens[0] in token_list["<s>"].next:
					temp_costs["<s>"] = {}
					temp_costs["<s>"][tokens[0]] = {}
					for language in token_list["<s>"].next[tokens[0]]:
						if language != "total":
							if language not in prediction["langs"]:
								prediction["langs"][language] = []
							prediction["langs"][language].append(tokens[0])
							if language not in prediction["totals"]:
								prediction["totals"][language] = 0
							if language not in temp_costs["<s>"][tokens[0]]:
								temp_costs["<s>"][tokens[0]][language] = 0
							prediction["totals"][language] = prediction["totals"][language] + (token_list["<s>"].next[tokens[0]][language]["num"] / token_list["<s>"].next[tokens[0]]["total"]) + token_list["<s>"].next[tokens[0]][language]["weight"]
				for i in range(1, len(tokens)):
					if tokens[i-1] in token_list:
						if tokens[i] in token_list[tokens[i-1]].next:
							temp_costs[tokens[i-1]] = {}
							temp_costs[tokens[i-1]][tokens[i]] = {}
							for Lang in token_list[tokens[i-1]].next[tokens[i]]:
								if Lang != "total":
									if Lang not in prediction["langs"]:
										prediction["langs"][Lang] = []
									prediction["langs"][Lang].append(tokens[i-1])
									if Lang not in prediction["totals"]:
										prediction["totals"][Lang] = 0
									if Lang not in temp_costs[tokens[i-1]][tokens[i]]:
										temp_costs[tokens[i-1]][tokens[i]][Lang] = 0
									prediction["totals"][Lang] = prediction["totals"][Lang] + (token_list[tokens[i-1]].next[tokens[i]][Lang]["num"] / token_list[tokens[i-1]].next[tokens[i]]["total"]) + token_list[tokens[i-1]].next[tokens[i]][Lang]["weight"]
						else:
							name = MapNode(tokens[i-1],lang)
							token_list[tokens[i-1]] = name
							node_list.append(name)
				sort = sorted(prediction["totals"].items(), key= lambda x: x[1], reverse=True)
				# print(sort)
				if len(sort) != 0:
					prediction["max"] = list(sort)[0][1]
					prediction["output"] = list(sort)[0][0]
					if(prediction["output"] != lang):
						print("Predicted language: " + prediction["output"])
						print("Actual language: " + lang)
						costs_per_lang = {}
						predicted = prediction["max"]
						# print(prediction["totals"])
						if lang not in prediction["totals"]:
							prediction["totals"][lang] = 0
							prediction["langs"][lang] = []
						actual = prediction["totals"][lang]
						for langs in prediction["totals"]:
							#print(len(prediction["langs"][lang]))
							if prediction["totals"][langs] >= actual:
								cost = actual - prediction["totals"][langs]
								if(langs == lang):
									cost = prediction["totals"][prediction["output"]] - actual
								prediction["net_cost"] = prediction["net_cost"] + abs(cost)
								if (len(prediction["langs"][langs]) != 0):
									costs_per_lang[langs] = cost / len(prediction["langs"][langs])
						net_cost += abs(prediction["net_cost"])
						vector_cost += prediction["net_cost"]
						for key in temp_costs:
							for token in temp_costs[key]:
								for lang1 in temp_costs[key][token]:
									# print(lang)
									if lang1 not in costs_per_lang:
										costs_per_lang[lang1] = 0
									temp_costs[key][token][lang1] += costs_per_lang[lang1]
									if key not in costs:
										costs[key] = {}
									if token not in costs[key]:
										costs[key][token] = {}
									if lang1 not in costs[key][token]:
										costs[key][token][lang1] = []
									costs[key][token][lang1].append(temp_costs[key][token][lang1])
					else:
						num_correct += 1
		except KeyError as k:
			raise k
	print(net_cost)
	percent = num_correct / total_num
	print("Percent correct: " + str(percent))
	costs_per_epoch[j+1] = net_cost
	# print(vector_cost)
	for key in costs:
		for token in costs[key]:
			for l in costs[key][token]:
				cost = 0
				for entry in costs[key][token][l]:
					cost = cost + entry
					avg_cost = cost / len(costs[key][token][l])
					# print(token_list[key].next[token][lang]["weight"])
					if token in token_list[key].next:
						if l in token_list[key].next[token]:
							# print(key)
							# print(token_list[key].next[token])
							token_list[key].next[token][l]["weight"] += (avg_cost * learning_rate)
							# print(token_list[key].next[token])
					# print(token_list[key].next[token][lang]["weight"])
	print("")
	#print(prediction)
for key, value in costs_per_epoch.items():
	print(str(key) + "," + str(value))