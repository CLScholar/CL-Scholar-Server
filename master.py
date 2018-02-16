import os
import sys
import re
import json
import datetime
from collections import defaultdict
from string import punctuation
from nltk.stem import PorterStemmer

ps = PorterStemmer()

authidnamesdict = {}

authidnamesdict = json.load(open('namedict.json','r'))

stopwords = ["a","an","the","in","at","of","for","on","and","is","by","was","are","were","do","did","does","where","when","who","which","what","have","has","had","trend","from","since","to","till","until","upto","field","fields","area","areas","topic","topics","list","top","publications","publication","paper","papers","citations","citation","year","prof.","dr.","dr","prof","count","max","maximum","most","highest","conference","institute"]

conferencetitlesdict = json.load(open('conferencenames.json','r'))

topicdict = json.load(open('topic_mapping.json','r'))

def main():
	# print("Inside Main")
	# sys.stdout.flush()
	while True:
		for line in sys.stdin:
			inputstr = line
			# print(line)
			# sys.stdout.flush()
			entity_recog(inputstr)

def entity_recog(querystr):
	# querystr = sys.argv[1]
	querystr = re.sub('[^A-Za-z0-9]',' ',querystr)
	querystr = querystr.strip()

	now = datetime.datetime.now()
	curr = int(now.year)

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

	relationship(outputstr)

def relationship(queries):

	top_synonyms=['highest', 'top', 'topmost', 'most', 'utmost', 'supreme', 'best', 'top-grade', 'premier', 'peerless', 'unrivalled', 'unsurpassed', 'finest', 'elite']
	most_synonyms=['most','maximum','largest','greatest','highest']
	field_synonyms=['field','topic','domain','area','sphere','branch','sector','discipline']
	conf_synonyms=['conference','workshop','symposium','summit','meeting','conclave','seminar','forum','convocation','school']
	publish_synonyms=['publish','publication','acceptance','accept']
	list_synonyms=['list','enlist','enumerate','tabulate','rank','what are']
	be_verb_synonyms=['is','was','are','were','do','does','did','has','have','had','will']
	future_verb_synonyms=['shall','would','can','could','should']
	author_synonyms=['author','researcher','scientist','person','engineer','linguist']
	paper_synonyms=['paper','work']
	number_synonyms=['number','no','distribution','trend']


	top_synonyms.extend([ps.stem(i.strip()) for i in top_synonyms])
	field_synonyms.extend([ps.stem(i.strip()) for i in field_synonyms])
	conf_synonyms.extend([ps.stem(i.strip()) for i in conf_synonyms])
	publish_synonyms.extend([ps.stem(i.strip()) for i in publish_synonyms])
	most_synonyms.extend([ps.stem(i.strip()) for i in most_synonyms])
	list_synonyms.extend([ps.stem(i.strip()) for i in list_synonyms])
	author_synonyms.extend([ps.stem(i.strip()) for i in author_synonyms])
	paper_synonyms.extend([ps.stem(i.strip()) for i in paper_synonyms])
	number_synonyms.extend([ps.stem(i.strip()) for i in number_synonyms])

	# queries=sys.argv[0]
	# Convert string to list
	queries = [queries]

	errCnt =0
	corCnt = 0

	stat_increment=0
	binary_increment=100
	list_increment=200

	auth_regex="([$][a][:][0-9,]+[$])"
	field_regex="([$][f][:][0-9,]+[$])"
	univ_regex="([$][u][:][0-9,]+[$])"
	venue_regex="([$][v][:][0-9,]+[$])"
	year_regex="([$][y][:][0-9,]+[$])"



	for query in queries:
		# line=line.strip().split('\t')
		# act_queryId = int(line[0])
		# query = line[1]
		query=re.sub('[^A-Za-z0-9$,:]',' ',query)
		query=query.strip().lower()
		words=query.split()
		stem_words=[ps.stem(i) for i in words]
		queryId=0
		# branch off the stems
		how_many_branch=0
		reg_auth=re.findall(auth_regex,query)
		reg_field=re.findall(field_regex,query)
		reg_venue=re.findall(venue_regex,query)
		reg_univ=re.findall(univ_regex,query)
		reg_year=re.findall(year_regex,query)



		type_dict={}
		type_dict['$a']=[]
		type_dict['$v']=[]
		type_dict['$f']=[]
		type_dict['$u']=[]
		type_dict['$y']=[]

		for elem in reg_auth:
			elem=elem.split(':')
			if elem[0] =='$a':
				type_dict['$a'].extend(elem[1].split(',')[:-1])

		for elem in reg_venue:
			elem=elem.split(':')
			if elem[0] =='$v':
				type_dict['$v'].extend(elem[1].split(',')[:-1])

		for elem in reg_univ:
			elem=elem.split(':')
			if elem[0]=='$u':
				type_dict['$u'].extend(elem[1].split(',')[:-1])

		for elem in reg_field:
			elem=elem.split(':')
			if elem[0] =='$f':
				type_dict['$f'].extend(elem[1].split(',')[:-1])

		for elem in reg_year:
			elem=elem.split(':')
			if elem[0] =='$y':
				type_dict['$y'].extend(elem[1].split(',')[:-1])


		### Check if it is statistical, binary or list:

		field_flag=0
		conf_flag=0
		pub_flag=0
		top_index=-1
		most_flag=0
		list_flag=0
		author_flag=0
		binary_flag=0
		paper_flag=0
		increment=-1
		number_index=-1

		for i, word in enumerate(stem_words):
			if ~field_flag:
				if word in field_synonyms:
					field_flag=1
			if ~conf_flag:
				if word in conf_synonyms:
					conf_flag=1
			if ~pub_flag:
				if word in publish_synonyms:
					pub_flag=1
			if ~most_flag:
				if word in most_synonyms:
					most_flag=1
			if ~list_flag:
				if word in list_synonyms:
					list_flag=1
			if ~paper_flag:
				if word in paper_synonyms:
					paper_flag=1
			if ~author_flag:
				if word in author_synonyms:
					author_flag=1
			if -1 == top_index:
				if word in top_synonyms:
					top_index = i
			if -1 == number_index:
				if word in number_synonyms:
					number_index = i

		whoFlag = 0
		if 'who' in stem_words:
			whoFlag = 1

		if 'which' in stem_words or whoFlag:
			if conf_flag:
				if pub_flag or paper_flag:
					if most_flag==1:
						queryId = 7
			elif paper_flag:
				if len(reg_field)>0:
					if 'citat' in stem_words:
						if most_flag==1:
							queryId = 9
			elif author_flag or whoFlag:
				if len(reg_field)>0:
					if 'citat' in stem_words:
						if most_flag==1:
							queryId = 13

		elif 'when' in stem_words:
			if pub_flag or paper_flag:
				if 'start' in stem_words:
					if len(reg_auth)>0:
						if len(reg_field)>0:
							queryId = 10

		# elif 'compar' in stem_words:
		# 	if len(reg_field)>0:
		# 		if len(reg_venue) == 2:
		# 			queryId = 3
		elif 'compar' in stem_words:
			if len(reg_field)>0:
				if len(reg_venue) == 2:
					queryId = 300
				elif len(reg_auth)==2:
					queryId=301
			elif ps.stem('impact') in stem_words and ps.stem('factor') in stem_words:
				if len(reg_venue)==2:
					queryId=302
		# else:
		# 	queryId=0
				# print 'whoFlag'
		if queryId==0:
			if words[0] in be_verb_synonyms:
				binary_flag=1
				increment=100

			elif 'how' in words and 'many' in words:
				how_ind=words.index('how')
				many_ind=words.index('many')
				if how_ind+1==many_ind:
					how_many_branch=1
					increment=0

			elif number_index>=0 and 'of' in words:
				# of_ind = words.index('of')
				if 'of'== words[number_index+1]:
					how_many_branch = 1
					increment=0

			elif list_flag==1:
				increment=200
			else:
				increment=-1

		if increment>=0:
			if len(reg_univ)>0:
				if len(reg_field)>0:
					queryId=22
				elif ps.stem('cite') in stem_words or ps.stem('citation') in stem_words:
					queryId=24
				elif field_flag==1:
					queryId=23
				elif pub_flag ==1 or paper_flag==1:
					queryId=25
				# else:
				# 	queryId=0

			elif len(reg_venue)>0 or conf_flag==1:
				if len(reg_venue)>0:
					if len(reg_field)>0:
						queryId=1
					elif field_flag==1:
						queryId=21
					elif top_index != -1 and paper_flag==1 :
						limit = int(stem_words[stem_words.index('top')+1])
						queryId = 14
						increment=200
					else:
						queryId=8
				else:
					if len(reg_field)>0:
						if len(reg_year)>0:
							queryId=19
						else:
							queryId=20


			elif len(reg_auth)>0:
				if  'sentiment' in stem_words:
					if 'posit' in stem_words:
						queryId = 16
					elif 'neg' in stem_words:
						queryId = 15
				elif len(reg_auth)==2:
						if len(reg_field)>0:
							queryId=12
						else:
							queryId=11
				else:
					if len(reg_field)>0:
						queryId=5
					else:
						queryId=4
			else:
				if len(reg_field)>0 and (pub_flag==1 or paper_flag==1):
					queryId=6

			queryId=queryId+increment

		outputarray = []
		outputarray.append(queryId)
		outputarray.append(type_dict)
		# print(queryId)
		print(outputarray)
		# sys.stdout.flush()
		# if queryId != act_queryId:
		# 	errCnt += 1
		# 	print(line[0],line[1])
		# 	print(queryId,act_queryId)
		# else:
		# 	corCnt +=1


	# print(errCnt, corCnt)

#start process
if __name__ == '__main__':
	main()
