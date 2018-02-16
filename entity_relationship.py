import re
from string import punctuation
from nltk.stem import PorterStemmer
ps = PorterStemmer()

top_synonyms= [ps.stem(i.strip()) for i in ['highest', ' top', ' topmost', ' most', ' utmost', ' supreme', ' best', ' top-grade', 'premier', ' peerless', ' unrivalled', ' unsurpassed', ' finest', ' elite']]
field_synonyms=[ps.stem(i.strip()) for i in ['field','topic','domain','area','sphere','branch','sector','discipline']]
conf_synonyms=[ps.stem(i.strip()) for i in ['conference','workshop','symposium','summit','meeting','conclave','seminar','forum','convocation','school']]
publish_synonyms=[ps.stem(i.strip()) for i in ['publish','publication','acceptance','accept']]

# query = "Which conference accepts maximum number of papers?"
# query = "When, $A$, has started, publishing in $F$?"
# query = "Compare $V$ and $V$ for $F$ papers over the year?"
# query = "Which paper on $f$ has most citations? "
# query = "Is $V$ accepting papers from $F$?"
# query = "Get the list of papers with negative sentiment score of an author $A$."
query = "List the top '12' papers in a venue $V$"
# query = raw_input()


# print punctuation
# print(query.strip(punctuation.replace('$', '')))
query = re.sub('[^A-Za-z0-9$]', ' ', query)
# query = re.sub('[^A-Za-z0-9$]+',' ',query)

words=query.strip().lower().split()
print (words)

# print (ps.stem('many,'))

stem_words = []
for word in words:
	stem_words.append(ps.stem(word))

print(stem_words)

# print(ps.stem('has') in stem_words)

# queryId

query_file=open('query_test.txt')

errCnt =0
corCnt = 0

for line in query_file:
	line=line.strip().split('\t')

	act_queryId = int(line[0])
	query = line[1]

	query=re.sub('[^A-Za-z0-9$]',' ',query)
	
	words=query.strip().lower().split()
	stem_words=[ps.stem(i) for i in words]

	queryId=0
	# branch off the stems 
	how_many_branch=0

	if 'how' in words and 'many' in words:
		how_ind=words.index('how')
		many_ind=words.index('many')
		if how_ind+1==many_ind:
			how_many_branch=1

	if ('number' in words or 'no' in words) and 'of' in words:
		of_ind = words.index('of')
		if 'number' in words:
			no_ind = words.index('number')
		else:
			no_ind = words.index('no')
		if no_ind+1 == of_ind:
			how_many_branch = 1



	field_flag=0
	conf_flag=0
	pub_flag=0
	top_index=-1
	for i, word in enumerate(stem_words):
		if ~field_flag:
			if word in field_synonyms:
				field_flag=1

	# for word in stem_words:
		if ~conf_flag:
			if word in conf_synonyms:
				conf_flag=1		

	# for word in stem_words:
		if ~pub_flag:
			if word in publish_synonyms:
				pub_flag=1

	# for i, word in stem_words:
		if -1 == top_index:
			if word in top_synonyms:
				top_index = i

	whoFlag = 0
	if 'who' in stem_words:
		whoFlag = 1
		# print 'whoFlag'
	
	


	if 'is' in stem_words:
		if pub_flag:
			if '$v$' in stem_words:
				if '$f$' in stem_words:
					queryId = 2

	elif 'list' in stem_words:
		if '$a$' in stem_words:
			if 'sentiment' in stem_words:
				if 'posit' in stem_words:
					queryId = 16
				elif 'neg' in stem_words:
					queryId = 15
		elif top_index != -1:
			limit = int(stem_words[stem_words.index('top')+1])
			if '$v$' in stem_words:
				queryId = 14

	elif 'when' in stem_words:
		if pub_flag:
			if 'start' in stem_words:
				if '$a$' in stem_words:
					if '$f$' in stem_words:
						queryId = 10

	elif 'compar' in stem_words:
		if '$f$' in stem_words:
			if stem_words.count('$v$') == 2:
				queryId = 3
			# if ps.stem('when') in stem_words:
				# if ps.stem('when') in stem_words:

	# who
		# if '$f$' in stem_words:
		#     if 'citat' in stem_words:
		#         if 'maximum' in stem_words or 'most' in stem_words:
		#             queryId = 13

	elif 'which' in stem_words or whoFlag:
		if conf_flag:
			if pub_flag:
				if 'maximum' in stem_words or 'most' in stem_words:
					queryId = 7
		elif 'paper' in stem_words:
			if '$f$' in stem_words:
				if 'citat' in stem_words:
					if 'maximum' in stem_words or 'most' in stem_words:
						queryId = 9
		elif 'author' in stem_words or whoFlag:
			if '$f$' in stem_words:
				if 'citat' in stem_words:
					if 'maximum' in stem_words or 'most' in stem_words:
						queryId = 13

						
	elif how_many_branch==1:
		if '$u$' in words:
			if '$f$' in words:
				queryId=22
			elif ps.stem('cite') in stem_words or ps.stem('citation') in stem_words:
				queryId=24
			elif field_flag==1:
				queryId=23
			elif pub_flag ==1:
				queryId=25
			else:
				queryId=0	

		elif '$v$' in words or conf_flag==1:
			if '$v$' in words:
				if '$f$' in words:
					queryId=1
				elif field_flag==1:
					queryId=21
				else:
					queryId=8
			else:
				if '$f$' in words:
					if '$y$' in words:
						queryId=19
					else:
						queryId=20	

		elif pub_flag ==1:
			if '$a$' in words:
				if words.count('$a$')==2:
					if '$f$' in words:
						queryId=12
					else:
						queryId=11
				else:
					if '$f$' in words:
						queryId=5
					else:
						queryId=4
			else:
				if '$f$' in words:
					queryId=6									
		
		# else:
		# 	queryId=0									

	print(line[0],line[1])		
	print(queryId,act_queryId)
	if queryId != act_queryId:
		errCnt += 1
	else:
		corCnt +=1

print errCnt, corCnt
# whoFlag = 0
# if 'who' in stem_words:
#     whoFlag = 1
#     print 'whoFlag'

# if 'is' in stem_words:
#     if 'accept' in stem_words:
#         if '$v$' in stem_words:
#             if '$f$' in stem_words:
#                 queryId = 2

# elif 'list' in stem_words:
#     if '$a$' in stem_words:
#         if 'sentiment' in stem_words:
#             if 'posit' in stem_words:
#                 queryId = 16
#             elif 'neg' in stem_words:
#                 queryId = 15
#     elif 'top' in stem_words:
#         limit = int(stem_words[stem_words.index('top')+1])
#         if '$v$' in stem_words:
#             queryId = 14

# elif 'when' in stem_words:
#     if 'publish' in stem_words:
#         if 'start' in stem_words:
#             if '$a$' in stem_words:
#                 if '$f$' in stem_words:
#                     queryId = 10

# elif 'compar' in stem_words:
#     if '$f$' in stem_words:
#         if stem_words.count('$v$') == 2:
#             queryId = 3
#         # if ps.stem('when') in stem_words:
#             # if ps.stem('when') in stem_words:

# # who
#     # if '$f$' in stem_words:
#     #     if 'citat' in stem_words:
#     #         if 'maximum' in stem_words or 'most' in stem_words:
#     #             queryId = 13

# elif 'which' in stem_words or whoFlag:
#     if 'confer' in stem_words:
#         if 'accept' in stem_words:
#             if 'maximum' in stem_words or 'most' in stem_words:
#                 queryId = 7
#     elif 'paper' in stem_words:
#         if '$f$' in stem_words:
#             if 'citat' in stem_words:
#                 if 'maximum' in stem_words or 'most' in stem_words:
#                     queryId = 9
#     elif 'author' in stem_words or whoFlag:
#         if '$f$' in stem_words:
#             if 'citat' in stem_words:
#                 if 'maximum' in stem_words or 'most' in stem_words:
#                     queryId = 13

# print ps.stem('maximum'), ps.stem('$a$')
# print ps.stem('when'), ps.stem('publish'), ps.stem('start'), ps.stem('$f$'), ps.stem('compare'), ps.stem('$v$'), ps.stem('which'), ps.stem('conference'), ps.stem('accept'), ps.stem('most')
# print queryId