from textblob import TextBlob
from textblob.classifiers import DecisionTreeClassifier
from textblob.classifiers import NaiveBayesClassifier
import sys
import os
import pickle
import cPickle
import nltk.classify
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.classify import SklearnClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.svm import SVC

def save_naiveclassifier(classifier):
	f = open('naivebayes_classifier.pickle', 'wb')
	cPickle.dump(classifier, f)
	f.close()

def load_naiveclassifier():
	f = open('naivebayes_classifier.pickle', 'rb')
	classifier = cPickle.load(f)
	f.close()
	return classifier

def save_decisionclassifier(classifier):
	f = open('decisiontree_classifier.pickle', 'wb')
	cPickle.dump(classifier, f)
	f.close()

def load_decisionclassifier():
	f = open('decisiontree_classifier.pickle', 'rb')
	classifier = cPickle.load(f)
	f.close()
	return classifier

def review_features(word):
        positivewords=[]
        negativewords=[]
        inverters=[]
        with open("positive-words.txt") as f:
            p= f.readlines()
        with open("negative-words.txt") as f:
            n= f.readlines()
        with open("inverters.txt") as f:
            inv= f.readlines()
        for x in p:
            x1=x.split('\n')
            x=x1[0].lower()
            positivewords.append(x)
        for x in n:
            x1=x.split('\n')
            x=x1[0].lower()
            negativewords.append(x)
        for x in inv:
            x1=x.split('\n')
            x=x1[0].lower()
            inverters.append(x)
        posi=0
        negi=0
        inver=0
        for words in word.split(" "):
            if words.lower() in positivewords:
                posi=posi+1
            if words.lower() in negativewords:
                negi=negi+1
            if words.lower() in inverters:
                inver=( inver+ 1 ) % 2 
        return {'positive': posi, 'negative': negi, 'inverters': inver}

reload(sys)
sys.setdefaultencoding('utf-8')

if os.path.exists('naivebayes_classifier.pickle'):
	print "file exist"
	naive = load_naiveclassifier()
else:
	train = []
	openfile= "rt-polarity.pos"
	i=0
	with open(openfile) as f:
		for line in f:
			line = unicode(line, errors='replace').replace('\n',"").replace('.'," ")
			train.append((line, "pos"))
			i=i+1
			if i== 500:
				break
		
	openfile= "rt-polarity.neg"
	i=0
	with open(openfile) as f:
		for line in f:
			line = unicode(line, errors='replace').replace('\n',"").replace('.'," ")
			train.append((line, "neg"))
			i=i+1
			if i== 500:
				break
	naive = NaiveBayesClassifier(train)
	save_naiveclassifier(naive)

print "Naive Bayes Trained"

if os.path.exists('decisiontree_classifier.pickle'):
	decision = load_decisionclassifier()
else:
	train = []
	openfile= "rt-polarity.pos"
	i=0
	with open(openfile) as f:
		for line in f:
			line = unicode(line, errors='replace').replace('\n',"").replace('.'," ")
			train.append((line, "pos"))
			i=i+1
			if i== 2000:
				break
		
	openfile= "rt-polarity.neg"
	i=0
	with open(openfile) as f:
		for line in f:
			line = unicode(line, errors='replace').replace('\n',"").replace('.'," ")
			train.append((line, "neg"))
			i=i+1
			if i== 2000:
				break
	random.seed(60221023)
	random.shuffle(train)
	featuresets = [(review_features(n), g) for (n,g) in train]
	train_set, test_set = featuresets[500:], featuresets[:500]
	print "Decision Tree Trained"
	decision=nltk.classify.DecisionTreeClassifier.train(train_set, entropy_cutoff=0,support_cutoff=0)
	save_decisionclassifier(classifier)
print "Decision Tree Classifier Trained"

with open("yelplinks.txt") as f:
    array= f.readlines()
for line in array:
    line1=line.split('\n')
    openfile= "wordstopolarity/"+line1[0]+".txt"
    outputfile = open ("polarity/"+line1[0]+".txt" , "w+")
    outputfiletest = open ("polaritytesting/"+line1[0]+".txt" , "w+")
    k=0
    with open(openfile) as s:
        for line in s:
			text = line
			if k % 200 ==0 :
				print line1[0]+ "\t"+str (k)
			k=k+1
			naivebayes=naive.prob_classify(text)
			naivebayes_max=naivebayes.max()
			naivebayes_prob=round(naivebayes.prob(naivebayes_max), 3)
			naivebayes_value=0
			if str(naivebayes_max)=="pos":
				naivebayes_value= 1
			else:
				naivebayes_value= -1

			decisionTest=[(review_features(text))]
			decisionTree=decision.classify_many(decisionTest)
			decisionTree_value=0
			if str(decisionTree[0])=="pos":
				decisionTree_value=1
			else:
				decisionTree_value= -1

			blob = TextBlob(text)
			polarity=0
			i=0
			for sentence in blob.sentences:
				polarity=polarity+sentence.sentiment.polarity
				i=i+1
			polarity=round(polarity/i, 3)
			
			if polarity > 0 :
				polarity_value = 1
			elif polarity == 0.0:
				polarity_value = 0
			else:
				polarity_value = -1
			answer=0
			if polarity_value==0:
				answer=0
			else:
				answer=naivebayes_value + decisionTree_value + polarity_value 
			if answer > 0 :
				if polarity > 0:
					answer=polarity
				else:
					answer=naivebayes_prob
				if polarity > 0 and naivebayes_prob > 0 :
					answer=(polarity+ naivebayes_prob)/2
			if answer < 0 :
				if polarity < 0:
					answer=polarity
				else:
					answer=naivebayes_prob
				if polarity < 0 and naivebayes_prob < 0 :
					answer=(polarity+ naivebayes_prob)/2
			value= str(line)+str(naivebayes_prob) + "\t" + str(decisionTree_value) + "\t"+str(polarity)+"\t"+str(answer)+"\n"
			outputfiletest.write(str(value))
			outputfiletest.write("\n")
			outputfile.write(str(answer))
			outputfile.write("\n")
	outputfile.close()
	outputfiletest.close()