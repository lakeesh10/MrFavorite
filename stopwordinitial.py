import nltk
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import tokenize


text_file1=open("stoplist.txt", "r")
stoplist=text_file1.read()
with open("yelplinks.txt") as f:
	array= f.readlines()
for line in array:
	link=line.split('\n')
	openfile= open("database/"+link[0]+".txt" , "r")
	document=openfile.read()
	sentences=tokenize.sent_tokenize(document)
	outputfile = open ("stopword/"+link[0]+".txt" , "w+")
	i=0
	for sentence in sentences:
		tagged_words=pos_tag(word_tokenize(sentence))
		struct=[]
		if i % 500 == 0:
			print link[0],i
		i=i+1
		listAdd = word_tokenize(" CC JJ JJR JJS NN NNP NNS NNPS RB WRB WP VBN " )
		for pairs in tagged_words:
			if pairs[1] in listAdd:
				struct.append(pairs[0])
		w_in_sen =nltk.word_tokenize(sentence.lower())
		importantwords = [word for word in w_in_sen if word not in stoplist or word in struct]
		#importantwords=[word for word in w_in_sen if word in listwords or word in struct]
		for x in importantwords:
			outputfile.write (x)
			outputfile.write (" ")
		outputfile.write ("\n")
	
	outputfile.close()