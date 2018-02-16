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
			if a >= 1950 and a < curr:
				yeartokens.append(a)
		except:
			if (token.lower() not in stopwords) or (token not in stopwords and token.lower() in stopwords):
				filtered.append(token.lower())

	marker = -1
	for token in filtered:
		for authid in authidnamesdict:
			if token in authidnamesdict[authid]:
				authidspertoken[token].append(authid)
			else:
				for name in authidnamesdict[authid]:
					if name.startswith(token,0):
						authidspertoken[token].append(authid)
						break

		for conferenceid in conferencetitlesdict:
			if token.upper() in conferencetitlesdict[conferenceid]:
				conferenceidspertoken[token].append(conferenceid)
				marker = 1
			elif len(token) > 1:
				marker=1
				counterforconf=0
				for char in token:
					temp=0
					counterforconf+=1
					for t in conferencetitlesdict[conferenceid]:
						if char.upper()==t[counterforconf-1]:
							temp = 1
							break
					if temp==0:
						marker=0
						break
				if marker==1:
					conferenceidspertoken[token].append(conferenceid)

		for topicid in topicdict:
			if token in topicdict[topicid]:
				topicidspertoken[token].append(topicid)
				marker = 1
			else:
				marker=1
				for char in token:
					temp=0
					for t in topicdict[topicid]:
						if t.startswith(char,0)==True:
							temp = 1
							break
					if temp==0:
						marker=0
						break
				if marker==1:
					topicidspertoken[token].append(topicid)
				


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
	field_synonyms=['field','topic','domain','area','sphere','branch','sector','discipline']
	conf_synonyms=['conference','workshop','symposium','summit','meeting','conclave','seminar','forum','convocation','school','venue']
	publish_synonyms=['publish','publication','acceptance','accept','conduct']
	list_synonyms=['list','enlist','enumerate','tabulate','rank','show','get','give']  #,'what'
	future_verb_synonyms=['shall','would','can','could','should']
	author_synonyms=['author','researcher','scientist','person','engineer','linguist']
	paper_synonyms=['paper','work','journal', 'article', 'demo']
	################################# EXTENDED PART UNDER TESTING ################
	most_synonyms=['most','maximum','largest','greatest','highest','best']
	more_synonyms=['more','greater','higher']
	less_synonyms=['less','lower','lesser']
	citation_synonyms=['citation','cite','reference','citations']
	first_synonyms=['first','start','started']
	last_synonyms=['last','end','latest']
	positive_synonyms=['positive','good','supporting','appreciating']
	negative_synonyms=['negative','bad','opposing','criticizing']
	until_synonyms=['until','till','upto','to']
	from_synonyms=['since','from']
	between_synonyms=['between','inbetween']
	number_synonyms=['number','no','distribution','trend']
	binary_synonyms=['is','was','are','were','do','does','did','has','have','had','will']

	most_synonyms.extend([ps.stem(i.strip()) for i in most_synonyms])
	more_synonyms.extend([ps.stem(i.strip()) for i in more_synonyms])
	less_synonyms.extend([ps.stem(i.strip()) for i in less_synonyms])
	citation_synonyms.extend([ps.stem(i.strip()) for i in citation_synonyms])
	first_synonyms.extend([ps.stem(i.strip()) for i in first_synonyms])
	last_synonyms.extend([ps.stem(i.strip()) for i in last_synonyms])
	positive_synonyms.extend([ps.stem(i.strip()) for i in positive_synonyms])
	negative_synonyms.extend([ps.stem(i.strip()) for i in negative_synonyms])
	until_synonyms.extend([ps.stem(i.strip()) for i in until_synonyms])
	from_synonyms.extend([ps.stem(i.strip()) for i in from_synonyms])
	between_synonyms.extend([ps.stem(i.strip()) for i in between_synonyms])
	binary_synonyms.extend([ps.stem(i.strip()) for i in binary_synonyms])

	most_flag=0
	more_flag=0
	less_flag=0
	cite_flag=0
	first_flag=0
	last_flag=0
	positive_flag=0
	negative_flag=0
	until_flag=0
	from_flag=0
	between_flag=0
	##############################################################################


	top_synonyms.extend([ps.stem(i.strip()) for i in top_synonyms])
	field_synonyms.extend([ps.stem(i.strip()) for i in field_synonyms])
	conf_synonyms.extend([ps.stem(i.strip()) for i in conf_synonyms])
	publish_synonyms.extend([ps.stem(i.strip()) for i in publish_synonyms])
	list_synonyms.extend([ps.stem(i.strip()) for i in list_synonyms])
	author_synonyms.extend([ps.stem(i.strip()) for i in author_synonyms])
	paper_synonyms.extend([ps.stem(i.strip()) for i in paper_synonyms])
	number_synonyms.extend([ps.stem(i.strip()) for i in number_synonyms])

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
	number_regex="([$][n][:][0-9,]+[$])"


	for query in queries:
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
		reg_number=re.findall(number_regex,query)



		type_dict={}
		type_dict['$a']=[]
		type_dict['$v']=[]
		type_dict['$f']=[]
		type_dict['$u']=[]
		type_dict['$y']=[]
		type_dict['$n']=[]

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

		for elem in reg_number:
			elem=elem.split(':')
			if elem[0] =='$n':
				type_dict['$n'].extend(elem[1].split(',')[:-1])


		### Check if it is statistical, binary or list:

		field_flag=0
		conf_flag=0
		pub_flag=0
		top_index=-1
		top_flag=0
		# most_flag=0
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
					top_flag=1
			if -1 == number_index:
				if word in number_synonyms:
					number_index = i
			if ~most_flag:
				if word in most_synonyms:
					most_flag=1
			if ~more_flag:
				if word in more_synonyms:
					more_flag=1
			if ~less_flag:
				if word in less_synonyms:
					less_flag=1
			if ~cite_flag:
				if word in citation_synonyms:
					cite_flag=1
			if ~first_flag:
				if word in first_synonyms:
					first_flag=1
			if ~last_flag:
				if word in last_synonyms:
					last_flag=1
			if ~positive_flag:
				if word in positive_synonyms:
					positive_flag=1
			if ~negative_flag:
				if word in negative_synonyms:
					negative_flag=1
			if ~until_flag:
				if word in until_synonyms:
					until_flag=1
			if ~from_flag:
				if word in from_synonyms:
					from_flag=1
			if ~between_flag:
				if word in between_synonyms:
					between_flag=1
			if 0 == i:
				if ~binary_flag:
					if word in binary_synonyms:
						binary_flag=1
					
		if ps.stem('impact') in stem_words:
			if most_flag==1:
				queryId=5025
			elif more_flag==1:
				queryId=6025
			elif less_flag==1:
				queryId=7025
			if queryId>0 and len(reg_year)==1:
				if until_flag==1:
					queryId += 600
				elif from_flag==1:
					queryId += 800
				else:
					queryId += 200
			elif queryId>0 and len(reg_year)==2:
				queryId += 400
				
		elif most_flag==1 or top_flag==1:
			if len(reg_number)==0:
				if paper_flag==1 or pub_flag==1:
					paper_flag=1
				if author_flag ==0 and conf_flag==0 and paper_flag==0:
					if cite_flag==1:
						if len(reg_venue) > 0:
							if len(reg_field) > 0:
								queryId =5007
							else:
								queryId =5003
						else:
							if len(reg_field) > 0:
								queryId =5005
							else:
								
								queryId =5001

				elif author_flag ==0 and conf_flag==0 and paper_flag==1:
					if cite_flag==1:
						if len(reg_auth) > 0:
							if len(reg_venue) > 0:
								if len(reg_field) > 0:
									queryId =5019
								else:
									queryId =5018
							else:
								if len(reg_field) > 0:
									queryId =5017
								else:
									queryId =5016
						else:
							if len(reg_venue) > 0:
								if len(reg_field) > 0:
									queryId =5020
								else:
									queryId =5015
							else:
								if len(reg_field) > 0:
									queryId =5014
								else:
									queryId =5013
					else:
						if len(reg_venue) > 0:
							if len(reg_field) > 0:
								queryId =5008
							else:
								queryId =5004
						else:
							if len(reg_field) > 0:
								queryId =5006
							else:
								queryId =5002
				elif author_flag ==0 and conf_flag==1 and paper_flag==0:
					if cite_flag==1:
						if len(reg_auth) > 0:
							if len(reg_field) > 0:
								queryId =5024
							else:
								queryId =5023
						else:
							if len(reg_field) > 0:
								queryId =5012
							else:
								queryId =5011
								
				elif author_flag ==0 and conf_flag==1 and paper_flag==1:
					if cite_flag==1:
						if len(reg_auth) > 0:
							if len(reg_field) > 0:
								queryId =5024
							else:
								queryId =5023
						else:
							if len(reg_field) > 0:
								queryId =5012
							else:
								queryId =5011
					else:
						if len(reg_auth) > 0:
							if len(reg_field) > 0:
								queryId =5022
							else:
								queryId =5021
						else:
							if len(reg_field) > 0:
								queryId =5010
							else:
								queryId =5009
				elif author_flag ==1 and conf_flag==0 and paper_flag==0:
					if cite_flag==1:
						if len(reg_venue) > 0:
							if len(reg_field) > 0:
								queryId =5007
							else:
								queryId =5003
						else:
							if len(reg_field) > 0:
								queryId =5005
							else:
								# print('Here 3')
								queryId =5001
				elif author_flag ==1 and conf_flag==0 and paper_flag==1:
					if cite_flag==1:
						if len(reg_venue) > 0:
							if len(reg_field) > 0:
								queryId =5007
							else:
								queryId =5003
						else:
							if len(reg_field) > 0:
								queryId =5005
							else:
								# print('Here 4')
								queryId =5001
					else:
						if len(reg_venue) > 0:
							if len(reg_field) > 0:
								queryId =5008
							else:
								queryId =5004
						else:
							if len(reg_field) > 0:
								queryId =5006
							else:
								queryId =5002
				elif author_flag ==1 and conf_flag==1 and paper_flag==0:
					pass
				elif author_flag ==1 and conf_flag==1 and paper_flag==1:
					pass
				if queryId>0 and len(reg_year)==1:
					if until_flag==1:
						queryId += 600
					elif from_flag==1:
						queryId += 800
					else:
						queryId += 200
				elif queryId>0 and len(reg_year)==2:
					queryId += 400
			else:
				if paper_flag==1 or pub_flag==1:
					paper_flag=1
				if author_flag ==0 and conf_flag==0 and paper_flag==0:
					if cite_flag==1:
						if len(reg_venue) > 0:
							if len(reg_field) > 0:
								queryId =10007
							else:
								queryId =10003
						else:
							if len(reg_field) > 0:
								queryId =10005
							else:
								
								queryId =10001

				elif author_flag ==0 and conf_flag==0 and paper_flag==1:
					if cite_flag==1:
						if len(reg_auth) > 0:
							if len(reg_venue) > 0:
								if len(reg_field) > 0:
									queryId =10019
								else:
									queryId =10018
							else:
								if len(reg_field) > 0:
									queryId =10017
								else:
									queryId =10016
						else:
							if len(reg_venue) > 0:
								if len(reg_field) > 0:
									queryId =10020
								else:
									queryId =10015
							else:
								if len(reg_field) > 0:
									queryId =10014
								else:
									queryId =10013
					else:
						if len(reg_venue) > 0:
							if len(reg_field) > 0:
								queryId =10008
							else:
								queryId =10004
						else:
							if len(reg_field) > 0:
								queryId =10006
							else:
								queryId =10002
				elif author_flag ==0 and conf_flag==1 and paper_flag==0:
					if cite_flag==1:
						if len(reg_auth) > 0:
							if len(reg_field) > 0:
								queryId =10024
							else:
								queryId =10023
						else:
							if len(reg_field) > 0:
								queryId =10012
							else:
								queryId =10011
								
				elif author_flag ==0 and conf_flag==1 and paper_flag==1:
					if cite_flag==1:
						if len(reg_auth) > 0:
							if len(reg_field) > 0:
								queryId =10024
							else:
								queryId =10023
						else:
							if len(reg_field) > 0:
								queryId =10012
							else:
								queryId =10011
					else:
						if len(reg_auth) > 0:
							if len(reg_field) > 0:
								queryId =10022
							else:
								queryId =10021
						else:
							if len(reg_field) > 0:
								queryId =10010
							else:
								queryId =10009
				elif author_flag ==1 and conf_flag==0 and paper_flag==0:
					if cite_flag==1:
						if len(reg_venue) > 0:
							if len(reg_field) > 0:
								queryId =10007
							else:
								queryId =10003
						else:
							if len(reg_field) > 0:
								queryId =10005
							else:
								# print('Here 3')
								queryId =10001
				elif author_flag ==1 and conf_flag==0 and paper_flag==1:
					if cite_flag==1:
						if len(reg_venue) > 0:
							if len(reg_field) > 0:
								queryId =10007
							else:
								queryId =10003
						else:
							if len(reg_field) > 0:
								queryId =10005
							else:
								# print('Here 4')
								queryId =10001
					else:
						if len(reg_venue) > 0:
							if len(reg_field) > 0:
								queryId =10008
							else:
								queryId =10004
						else:
							if len(reg_field) > 0:
								queryId =10006
							else:
								queryId =10002
				elif author_flag ==1 and conf_flag==1 and paper_flag==0:
					pass
				elif author_flag ==1 and conf_flag==1 and paper_flag==1:
					pass
				if queryId>0 and len(reg_year)==1:
					if until_flag==1:
						queryId += 600
					elif from_flag==1:
						queryId += 800
					else:
						queryId += 200
				elif queryId>0 and len(reg_year)==2:
					queryId += 400

		elif more_flag==1 or less_flag==1:
			if paper_flag==1 or pub_flag==1:
				paper_flag=1
			if author_flag ==0 and conf_flag==0 and paper_flag==0:
				if cite_flag==1:
					if len(reg_venue) > 0:
						if len(reg_field) > 0:
							queryId =5007
						else:
							queryId =5003
					else:
						if len(reg_field) > 0:
							queryId =5005
						else:
							
							queryId =5001

			elif author_flag ==0 and conf_flag==0 and paper_flag==1:
				if cite_flag==1:
					if len(reg_auth) > 0:
						if len(reg_venue) > 0:
							if len(reg_field) > 0:
								queryId =5019
							else:
								queryId =5018
						else:
							if len(reg_field) > 0:
								queryId =5017
							else:
								queryId =5016
					else:
						if len(reg_venue) > 0:
							if len(reg_field) > 0:
								queryId =5020
							else:
								queryId =5015
						else:
							if len(reg_field) > 0:
								queryId =5014
							else:
								queryId =5013
				else:
					if len(reg_venue) > 0:
						if len(reg_field) > 0:
							queryId =5008
						else:
							queryId =5004
					else:
						if len(reg_field) > 0:
							queryId =5006
						else:
							queryId =5002
			elif author_flag ==0 and conf_flag==1 and paper_flag==0:
				if cite_flag==1:
					if len(reg_auth) > 0:
						if len(reg_field) > 0:
							queryId =5024
						else:
							queryId =5023
					else:
						if len(reg_field) > 0:
							queryId =5012
						else:
							queryId =5011
							
			elif author_flag ==0 and conf_flag==1 and paper_flag==1:
				if cite_flag==1:
					if len(reg_auth) > 0:
						if len(reg_field) > 0:
							queryId =5024
						else:
							queryId =5023
					else:
						if len(reg_field) > 0:
							queryId =5012
						else:
							queryId =5011
				else:
					if len(reg_auth) > 0:
						if len(reg_field) > 0:
							queryId =5022
						else:
							queryId =5021
					else:
						if len(reg_field) > 0:
							queryId =5010
						else:
							queryId =5009
			elif author_flag ==1 and conf_flag==0 and paper_flag==0:
				if cite_flag==1:
					if len(reg_venue) > 0:
						if len(reg_field) > 0:
							queryId =5007
						else:
							queryId =5003
					else:
						if len(reg_field) > 0:
							queryId =5005
						else:
							# print('Here 3')
							queryId =5001
			elif author_flag ==1 and conf_flag==0 and paper_flag==1:
				if cite_flag==1:
					if len(reg_venue) > 0:
						if len(reg_field) > 0:
							queryId =5007
						else:
							queryId =5003
					else:
						if len(reg_field) > 0:
							queryId =5005
						else:
							# print('Here 4')
							queryId =5001
				else:
					if len(reg_venue) > 0:
						if len(reg_field) > 0:
							queryId =5008
						else:
							queryId =5004
					else:
						if len(reg_field) > 0:
							queryId =5006
						else:
							queryId =5002
			elif author_flag ==1 and conf_flag==1 and paper_flag==0:
				pass
			elif author_flag ==1 and conf_flag==1 and paper_flag==1:
				pass
			if more_flag==1 and queryId>0:
				if len(reg_number) > 0:
					queryId += 1000
				elif queryId >=5001 and queryId <=5008 and len(reg_auth) > 0:
					queryId += 3000
				elif queryId >=5009 and queryId <=5012 and len(reg_venue) > 0:
					queryId += 3000
				elif queryId >=5021 and queryId <=5024 and len(reg_auth) > 0:
					queryId += 3000
			elif less_flag==1 and queryId>0:
				if len(reg_number) > 0:
					queryId += 2000
				elif queryId >=5001 and queryId <=5008 and len(reg_auth) > 0:
					queryId += 4000
				elif queryId >=5009 and queryId <=5012 and len(reg_venue) > 0:
					queryId += 4000
				elif queryId >=5021 and queryId <=5024 and len(reg_auth) > 0:
					queryId += 4000
			if queryId>0 and len(reg_year)==1:
				if until_flag==1:
					queryId += 600
				elif from_flag==1:
					queryId += 800
				else:
					queryId += 200
			elif queryId>0 and len(reg_year)==2:
				queryId += 400

		elif ps.stem('when')in stem_words:
			if paper_flag==1 or pub_flag==1:
				paper_flag=1
				if first_flag==1:
					if len(reg_auth) > 0:
						if len(reg_field) > 0:
							if len(reg_venue) > 0:
								queryId=4004
							else:
								queryId=4002
						elif len(reg_venue) > 0:
							queryId=4003
						else:
							queryId=4001
					elif len(reg_field) > 0:
						if len(reg_venue) > 0:
							queryId=4008
						else:
							queryId=4010
					elif len(reg_venue) > 0:
						queryId=4006
				elif last_flag==1:
					if len(reg_auth) > 0:
						if len(reg_field) > 0:
							if len(reg_venue) > 0:
								queryId=4014
							else:
								queryId=4012
						elif len(reg_venue) > 0:
							queryId=4005
						else:
							queryId=4013
					elif len(reg_field) > 0:
						if len(reg_venue) > 0:
							queryId=4009
						else:
							queryId=4011
					elif len(reg_venue) > 0:
						queryId=4007

		elif list_flag==1:
			if positive_flag==1:
				if len(reg_auth) > 0:
					if len(reg_field) > 0:
						if len(reg_venue) > 0:
							queryId=2020
						else:
							queryId=2019
					elif len(reg_venue) > 0:
						queryId=2017
					else:
						queryId=2015
				elif len(reg_field) > 0:
					if len(reg_venue) > 0:
						queryId=2018
					else:
						queryId=2016
				elif len(reg_venue) > 0:
					queryId=2014
				if len(reg_auth) > 1:
					if len(reg_venue)==0: 
						if len(reg_field)==0:
							queryId=2021
						else:
							queryId=2023
					else:
						if len(reg_field)==0:
							queryId=2022
						else:
							queryId=2024
				elif len(reg_venue) > 1:
					if len(reg_field)==0:
						queryId=2025
					else:
						queryId=2026
			elif negative_flag==1:
				if len(reg_auth) > 0:
					if len(reg_field) > 0:
						if len(reg_venue) > 0:
							queryId=2033
						else:
							queryId=2032
					elif len(reg_venue) > 0:
						queryId=2030
					else:
						queryId=2028
				elif len(reg_field) > 0:
					if len(reg_venue) > 0:
						queryId=2031
					else:
						queryId=2029
				elif len(reg_venue) > 0:
					queryId=2027
				if len(reg_auth) > 1:
					if len(reg_venue)==0: 
						if len(reg_field)==0:
							queryId=2034
						else:
							queryId=2036
					else:
						if len(reg_field)==0:
							queryId=2035
						else:
							queryId=2037
				elif len(reg_venue) > 1:
					if len(reg_field)==0:
						queryId=2038
					else:
						queryId=2039
			if paper_flag==1 or pub_flag==1:
				paper_flag=1
				if len(reg_auth) > 0:
					if len(reg_field) > 0:
						if len(reg_venue) > 0:
							queryId=2007
						else:
							queryId=2006
					elif len(reg_venue) > 0:
						queryId=2004
					else:
						queryId=2002
				elif len(reg_field) > 0:
					if len(reg_venue) > 0:
						queryId=2005
					else:
						queryId=2003
				elif len(reg_venue) > 0:
					queryId=2001

				if len(reg_auth) > 1:
					if len(reg_venue)==0: 
						if len(reg_field)==0:
							queryId=2008
						else:
							queryId=2010
					else:
						if len(reg_field)==0:
							queryId=2009
						else:
							queryId=2011
				elif len(reg_venue) > 1:
					if len(reg_field)==0:
						queryId=2012
					else:
						queryId=2013
			if queryId>0 and len(reg_year)==1:
				if until_flag==1:
					queryId += 600
				elif from_flag==1:
					queryId += 800
				else:
					queryId += 200
			elif queryId>0 and len(reg_year)==2:
				queryId += 400

		elif ps.stem('how') in stem_words or number_index >= 0:
			if positive_flag==1:
				if len(reg_auth) > 0:
					if len(reg_field) > 0:
						if len(reg_venue) > 0:
							queryId=20
						else:
							queryId=19
					elif len(reg_venue) > 0:
						queryId=17
					else:
						queryId=15
				elif len(reg_field) > 0:
					if len(reg_venue) > 0:
						queryId=18
					else:
						queryId=16
				elif len(reg_venue) > 0:
					queryId=14
				if len(reg_auth) > 1:
					if len(reg_venue)==0: 
						if len(reg_field)==0:
							queryId=21
						else:
							queryId=23
					else:
						if len(reg_field)==0:
							queryId=22
						else:
							queryId=24
				elif len(reg_venue) > 1:
					if len(reg_field)==0:
						queryId=25
					else:
						queryId=26
			elif negative_flag==1:
				if len(reg_auth) > 0:
					if len(reg_field) > 0:
						if len(reg_venue) > 0:
							queryId=33
						else:
							queryId=32
					elif len(reg_venue) > 0:
						queryId=30
					else:
						queryId=28
				elif len(reg_field) > 0:
					if len(reg_venue) > 0:
						queryId=31
					else:
						queryId=29
				elif len(reg_venue) > 0:
					queryId=27
				if len(reg_auth) > 1:
					if len(reg_venue)==0: 
						if len(reg_field)==0:
							queryId=34
						else:
							queryId=36
					else:
						if len(reg_field)==0:
							queryId=35
						else:
							queryId=37
				elif len(reg_venue) > 1:
					if len(reg_field)==0:
						queryId=38
					else:
						queryId=39		
			elif paper_flag==1 or pub_flag==1 or cite_flag==1:
				if paper_flag==1 or pub_flag==1:
					paper_flag=1
				if len(reg_auth) > 0:
					if len(reg_field) > 0:
						if len(reg_venue) > 0:
							queryId=7
						else:
							queryId=6
					elif len(reg_venue) > 0:
						queryId=4
					else:
						queryId=2
				elif len(reg_field) > 0:
					if len(reg_venue) > 0:
						queryId=5
					else:
						queryId=3
				elif len(reg_venue) > 0:
					queryId=1

				if len(reg_auth) > 1:
					if len(reg_venue)==0: 
						if len(reg_field)==0:
							queryId=8
						else:
							queryId=10
					else:
						if len(reg_field)==0:
							queryId=9
						else:
							queryId=11
				elif len(reg_venue) > 1:
					if len(reg_field)==0:
						queryId=12
					else:
						queryId=13
			if paper_flag==0:
				queryId+=100
			elif ps.stem('citation') in stem_words:
				if stem_words.index(ps.stem('paper')) > stem_words.index(ps.stem('citation')):
					queryId+=100
			if queryId>0 and len(reg_year)==1:
				if until_flag==1:
					queryId += 600
				elif from_flag==1:
					queryId += 800
				else:
					queryId += 200
			elif queryId>0 and len(reg_year)==2:
				queryId += 400

		elif ps.stem('compare') in stem_words:
			if cite_flag==1:
				if len(reg_auth) > 1:
					if len(reg_field) > 0:
						if len(reg_venue) > 0:
							queryId=3008
						else:
							queryId=3006
					elif len(reg_venue) > 0:
						queryId=3003
					else:
						queryId=3001
				if len(reg_venue) > 1:
					if len(reg_field) > 0:
						queryId=3012
					else:
						queryId=3010
			elif pub_flag==1 or paper_flag==1:
				if len(reg_auth) > 1:
					if len(reg_field) > 0:
						if len(reg_venue) > 0:
							queryId=3009
						else:
							queryId=3007
					elif len(reg_venue) > 0:
						queryId=3004
					else:
						queryId=3002
				if len(reg_venue) > 1:
					if len(reg_field) > 0:
						queryId=3013
					else:
						queryId=3011

		if queryId==0:
			if cite_flag==1:
				if positive_flag==1:
					if len(reg_auth) > 0:
						if len(reg_field) > 0:
							if len(reg_venue) > 0:
								queryId=20
							else:
								queryId=19
						elif len(reg_venue) > 0:
							queryId=17
						else:
							queryId=15
					elif len(reg_field) > 0:
						if len(reg_venue) > 0:
							queryId=18
						else:
							queryId=16
					elif len(reg_venue) > 0:
						queryId=14
					if len(reg_auth) > 1:
						if len(reg_venue)==0: 
							if len(reg_field)==0:
								queryId=21
							else:
								queryId=23
						else:
							if len(reg_field)==0:
								queryId=22
							else:
								queryId=24
					elif len(reg_venue) > 1:
						if len(reg_field)==0:
							queryId=25
						else:
							queryId=26
				elif negative_flag==1:
					if len(reg_auth) > 0:
						if len(reg_field) > 0:
							if len(reg_venue) > 0:
								queryId=33
							else:
								queryId=32
						elif len(reg_venue) > 0:
							queryId=30
						else:
							queryId=28
					elif len(reg_field) > 0:
						if len(reg_venue) > 0:
							queryId=31
						else:
							queryId=29
					elif len(reg_venue) > 0:
						queryId=27
					if len(reg_auth) > 1:
						if len(reg_venue)==0: 
							if len(reg_field)==0:
								queryId=34
							else:
								queryId=36
						else:
							if len(reg_field)==0:
								queryId=35
							else:
								queryId=37
					elif len(reg_venue) > 1:
						if len(reg_field)==0:
							queryId=38
						else:
							queryId=39		
				else:
					if len(reg_auth) > 0:
						if len(reg_field) > 0:
							if len(reg_venue) > 0:
								queryId=7
							else:
								queryId=6
						elif len(reg_venue) > 0:
							queryId=4
						else:
							queryId=2
					elif len(reg_field) > 0:
						if len(reg_venue) > 0:
							queryId=5
						else:
							queryId=3
					elif len(reg_venue) > 0:
						queryId=1

					if len(reg_auth) > 1:
						if len(reg_venue)==0: 
							if len(reg_field)==0:
								queryId=8
							else:
								queryId=10
						else:
							if len(reg_field)==0:
								queryId=9
							else:
								queryId=11
					elif len(reg_venue) > 1:
						if len(reg_field)==0:
							queryId=12
						else:
							queryId=13
				if paper_flag==0:
					queryId+=100
				elif stem_words.index(ps.stem('paper')) > stem_words.index(ps.stem('citation')):
					queryId+=100

			elif paper_flag==1 or pub_flag==1:
				if positive_flag==1:
					if len(reg_auth) > 0:
						if len(reg_field) > 0:
							if len(reg_venue) > 0:
								queryId=2020
							else:
								queryId=2019
						elif len(reg_venue) > 0:
							queryId=2017
						else:
							queryId=2015
					elif len(reg_field) > 0:
						if len(reg_venue) > 0:
							queryId=2018
						else:
							queryId=2016
					elif len(reg_venue) > 0:
						queryId=2014
					if len(reg_auth) > 1:
						if len(reg_venue)==0: 
							if len(reg_field)==0:
								queryId=2021
							else:
								queryId=2023
						else:
							if len(reg_field)==0:
								queryId=2022
							else:
								queryId=2024
					elif len(reg_venue) > 1:
						if len(reg_field)==0:
							queryId=2025
						else:
							queryId=2026
				elif negative_flag==1:
					if len(reg_auth) > 0:
						if len(reg_field) > 0:
							if len(reg_venue) > 0:
								queryId=2033
							else:
								queryId=2032
						elif len(reg_venue) > 0:
							queryId=2030
						else:
							queryId=2028
					elif len(reg_field) > 0:
						if len(reg_venue) > 0:
							queryId=2031
						else:
							queryId=2029
					elif len(reg_venue) > 0:
						queryId=2027
					if len(reg_auth) > 1:
						if len(reg_venue)==0: 
							if len(reg_field)==0:
								queryId=2034
							else:
								queryId=2036
						else:
							if len(reg_field)==0:
								queryId=2035
							else:
								queryId=2037
					elif len(reg_venue) > 1:
						if len(reg_field)==0:
							queryId=2038
						else:
							queryId=2039
				elif paper_flag==1 or pub_flag==1:
					paper_flag=1
					if len(reg_auth) > 0:
						if len(reg_field) > 0:
							if len(reg_venue) > 0:
								queryId=2007
							else:
								queryId=2006
						elif len(reg_venue) > 0:
							queryId=2004
						else:
							queryId=2002
					elif len(reg_field) > 0:
						if len(reg_venue) > 0:
							queryId=2005
						else:
							queryId=2003
					elif len(reg_venue) > 0:
						queryId=2001

					if len(reg_auth) > 1:
						if len(reg_venue)==0: 
							if len(reg_field)==0:
								queryId=2008
							else:
								queryId=2010
						else:
							if len(reg_field)==0:
								queryId=2009
							else:
								queryId=2011
					elif len(reg_venue) > 1:
						if len(reg_field)==0:
							queryId=2012
						else:
							queryId=2013

			elif len(reg_auth) > 0:
				queryId=50001
			elif len(reg_venue) > 0:
				queryId=50002

			if queryId>0 and len(reg_year)==1:
				if until_flag==1:
					queryId += 600
				elif from_flag==1:
					queryId += 800
				else:
					queryId += 200
			elif queryId>0 and len(reg_year)==2:
				queryId += 400

		if 1 == binary_flag:
			if queryId > 2000 and queryId < 3000:
				queryId += 9000	# 11000 Series
			elif queryId < 1000:
				queryId += 1000	# 1000 Series

		outputarray = []
		outputarray.append(queryId)
		outputarray.append(type_dict)
		print(outputarray)

#start process
if __name__ == '__main__':
	entity_recog(sys.argv[1])
