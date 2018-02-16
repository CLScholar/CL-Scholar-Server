import os
import sys
import re
from collections import defaultdict
import json
import datetime


def main():
	querystr = sys.argv[1]
	querystr = re.sub('[^A-Za-z0-9]',' ',querystr)
	querystr = querystr.strip()

	now = datetime.datetime.now()
	curr = int(now.year)

	authidnamesdict = {}

	authidnamesdict = json.load(open('namedict.json','r'))

	stopwords = ["a","an","the","in","at","of","for","on","and","is","by","was","are","were","do","did","does","where","when","who","which","what","have","has","had","trend","from","since","to","till","until","upto","field","fields","area","areas","topic","topics","list","top","publications","publication","paper","papers","citations","citation","year","prof.","dr.","dr","prof","count","max","maximum","most","highest","conference","institute"]

	conferencetitlesdict = json.load(open('conferencenames.json','r'))

	topicdict = json.load(open('topic_mapping.json','r'))

	authidspertoken = defaultdict(list)

	conferenceidspertoken = defaultdict(list)

	topicidspertoken = defaultdict(list)

	tokens = querystr.split()
	yeartokens = []

	filtered = []
	for token in tokens:
		try:
			a = int(token)
			if a >= 1900 and a < curr:
				yeartokens.append(a)
		except:
			if (token.lower() not in stopwords) or (token not in stopwords and token.lower() in stopwords):
				filtered.append(token.lower())

	marker = -1
	for token in filtered:
		for authid in authidnamesdict:
			if token in authidnamesdict[authid]:
				authidspertoken[token].append(authid)
			# else:
			# 	for name in authidnamesdict[authid]:
			# 		if name.startswith(token,0):
			# 			authidspertoken[token].append(authid)
			# 			break

		for conferenceid in conferencetitlesdict:
			if token.upper() in conferencetitlesdict[conferenceid]:
				conferenceidspertoken[token].append(conferenceid)
				marker = 1

		for topicid in topicdict:
			if token in topicdict[topicid]:
				topicidspertoken[token].append(topicid)
				marker = 1

	i=0
	longestlengthmatchfromtoken = defaultdict(list)
	authmatchlength = defaultdict(int)
	while i < len(filtered):
		j = i+1
		intersection = [x for x in authidspertoken[filtered[i]]]
		removable = []
		while j < len(filtered):
			for authid in intersection:
				if authid not in authidspertoken[filtered[j]]:
					removable.append(authid)
			for authid in removable:
				intersection.remove(authid)
			removable = []
			if len(intersection) > 0:
				j = j + 1
				for authid in intersection:
					longestlengthmatchfromtoken[filtered[i]].append(authid)
				authmatchlength[filtered[i]] += 1
			else:
				break
		i = i+1

	i=0
	longestlengthmatchfromtokenconf = defaultdict(list)
	confmatchlength = defaultdict(int)
	while i < len(filtered):
		j = i+1
		intersection = [x for x in conferenceidspertoken[filtered[i]]]
		removable = []
		while j < len(filtered):
			for confid in intersection:
				if confid not in conferenceidspertoken[filtered[j]]:
					removable.append(confid)
			for confid in removable:
				intersection.remove(confid)
			removable = []
			if len(intersection) > 0:
				j = j + 1
				for confid in intersection:
					longestlengthmatchfromtokenconf[filtered[i]].append(confid)
				confmatchlength[filtered[i]] += 1
			else:
				break
		i = i+1

	i=0
	longestlengthmatchfromtokentopic = defaultdict(list)
	topicmatchlength = defaultdict(int)
	while i < len(filtered):
		j = i+1
		intersection = [x for x in topicidspertoken[filtered[i]]]
		removable = []
		while j < len(filtered):
			for topicid in intersection:
				if topicid not in topicidspertoken[filtered[j]]:
					removable.append(topicid)
			for topicid in removable:
				intersection.remove(topicid)
			removable = []
			if len(intersection) > 0:
				j = j + 1
				for topicid in intersection:
					longestlengthmatchfromtokentopic[filtered[i]].append(topicid)
				topicmatchlength[filtered[i]] += 1
			else:
				break
		i = i+1

	tokens = querystr.split(" ")
	outputstr = ""
	if len(longestlengthmatchfromtoken) > 0:
		max_key = max(longestlengthmatchfromtoken, key= lambda x: authmatchlength[x])
		length = authmatchlength[max_key]
	else:
		max_key = ""
		length = 0
	if len(longestlengthmatchfromtokenconf) > 0:
		max_key_conf = max(longestlengthmatchfromtokenconf, key= lambda x: confmatchlength[x])
		length_conf = confmatchlength[max_key]
	else:
		max_key_conf = ""
		length_conf = 0
	if len(longestlengthmatchfromtokentopic) > 0:
		max_key_topic = max(longestlengthmatchfromtokentopic, key= lambda x: topicmatchlength[x])
		length_topic = topicmatchlength[max_key_topic]
	else:
		max_key_topic = ""
		length_topic = 0

	skip = 0
	authlist = []
	conflist = []
	topiclist = []
	for token in tokens:
		if skip != 0:
			skip -= 1
			if authmatchlength[token.lower()] == length:
				skip = length
				authlist += longestlengthmatchfromtoken[token.lower()]
			if confmatchlength[token.lower()] == length_conf:
				skip = max(length_conf,skip)
				conflist += longestlengthmatchfromtokenconf[token.lower()]
			if topicmatchlength[token.lower()] == length_topic:
				skip = max(length_topic,skip)
				conflist += longestlengthmatchfromtokentopic[token.lower()]
			if skip == 0:
				if len(authlist) > 0 :
					outputstr += "$A:"
					for auth in authlist:
						outputstr+= str(auth) + ","
					outputstr +="$ "

				if len(conflist) > 0 :
					outputstr += "$V:"
					for conf in conflist:
						outputstr+= str(conf) + ","
					outputstr +="$ "

				if len(topiclist) > 0 :
					outputstr += "$F:"
					for topic in topiclist:
						outputstr+= str(topic) + ","
					outputstr +="$ "
				authlist = []
				conflist = []
				topiclist = []
			continue
		try:
			a = int(token)
			if a in yeartokens:
				outputstr += "$Y:" + token + ",$ "
			else:
				outputstr+="$N:" + token +",$ "
		except:
			if (token.lower() not in stopwords) or (token not in stopwords and token.lower() in stopwords):
				check = True
				if length > 0:
					if authmatchlength[token.lower()] == length:
						skip = length
						authlist += longestlengthmatchfromtoken[token.lower()]
						check = False
				# else:
				# 	if len(authidspertoken[token.lower()]) > 0 :
				# 		outputstr += "$A:"
				# 		for conf in authidspertoken[token.lower()]:
				# 			outputstr+= str(conf) + ","
				# 		outputstr +="$ "
				# 		check = False
				if length_conf > 0:
					if confmatchlength[token.lower()] == length_conf:
						skip = max(length_conf,skip)
						conflist += longestlengthmatchfromtokenconf[token.lower()]
						check = False
				else:
					if len(conferenceidspertoken[token.lower()]) > 0 :
						outputstr += "$V:"
						for conf in conferenceidspertoken[token.lower()]:
							outputstr+= str(conf) + ","
						outputstr +="$ "
						check = False
				if length_topic > 0:
					if topicmatchlength[token.lower()] == length_topic:
						skip = max(length_topic,skip)
						topiclist += longestlengthmatchfromtokentopic[token.lower()]
						check = False
					elif check == True:
						outputstr += token + " "
				else:
					if len(topicidspertoken[token.lower()]) > 0 :
						outputstr += "$F:"
						for topic in topicidspertoken[token.lower()]:
							outputstr+= str(topic) + ","
						outputstr +="$ "
						check = False
					else:
						if check == True:
							outputstr += token + " "
			else:
				outputstr += token + " "

	print(outputstr)

#start process
if __name__ == '__main__':
	main()
