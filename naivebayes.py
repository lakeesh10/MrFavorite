from textblob import TextBlob
from textblob.classifiers import DecisionTreeClassifier
from textblob.classifiers import NaiveBayesClassifier
from textblob.en.sentiments import NaiveBayesAnalyzer
import sys
import os
import pickle
import cPickle
import nltk.classify
from sklearn.svm import LinearSVC
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk.classify import SklearnClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.svm import SVC

def word_feats(words):
    return dict([(word, True) for word in words])

def save_naiveclassifier(classifier):
	f = open('/home/lakeesh10/Documents/projectdemo/naivebayes_classifier.pickle', 'wb')
	cPickle.dump(classifier, f)
	f.close()

def load_naiveclassifier():
	f = open('/home/lakeesh10/Documents/projectdemo/naivebayes_classifier.pickle', 'rb')
	classifier = cPickle.load(f)
	f.close()
	return classifier
def save_svmclassifier(classifier):
	f = open('/home/lakeesh10/Documents/projectdemo/svm_classifier.pickle', 'wb')
	cPickle.dump(classifier, f)
	f.close()

def load_svmclassifier():
	f = open('/home/lakeesh10/Documents/projectdemo/svm_classifier.pickle', 'rb')
	classifier = cPickle.load(f)
	f.close()
	return classifier

def save_decisionclassifier(classifier):
	f = open('/home/lakeesh10/Documents/projectdemo/decisiontree_classifier.pickle', 'wb')
	cPickle.dump(classifier, f)
	f.close()

def load_decisionclassifier():
	f = open('/home/lakeesh10/Documents/projectdemo/decisiontree_classifier.pickle', 'rb')
	classifier = cPickle.load(f)
	f.close()
	return classifier

reload(sys)
sys.setdefaultencoding('utf-8')

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

if os.path.exists('/home/lakeesh10/Documents/projectdemo/naivebayes_classifier.pickle'):
	print "file exist"
	naive = load_naiveclassifier()
else:
	naive = NaiveBayesClassifier(train)
	save_naiveclassifier(naive)
print "Naive Bayes Trained"

if os.path.exists('/home/lakeesh10/Documents/projectdemo/decisiontree_classifier.pickle'):
	decision = load_decisionclassifier()
else:
	decision = DecisionTreeClassifier(train)
	save_decisionclassifier(decision)
print "Decision Tree Trained"

print("Naive Bayes : ",naive.classify("fried chip good and crunchy dig thattaco tropical omg so eyeopening"))
#print(decision.classify("fried chip good and crunchy dig thattaco tropical omg so eyeopening"))
cl=NaiveBayesAnalyzer()
print (cl.analyze("fried chip good and crunchy dig thattaco tropical omg so eyeopening"))
blob = TextBlob("fried chip good and crunchy dig thattaco tropical omg so eyeopening")
polarity=0
i=0
for sentence in blob.sentences:
	polarity=polarity+sentence.sentiment.polarity
	i=i+1
polarity=polarity/i 
print(polarity)

negids = movie_reviews.fileids('neg')
posids = movie_reviews.fileids('pos')
 
negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]
 
negcutoff = len(negfeats)*3/4
poscutoff = len(posfeats)*3/4
 
trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]

classifier = nltk.classify.SklearnClassifier(LinearSVC())

#print 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))
classifier.train(trainfeats)
#print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
#classif = SklearnClassifier(SVC(), sparse=False).train(trainfeats)
#print classif.classify_many(word_feats("fried chip good and crunchy dig thattaco tropical omg so eyeopening"))
print classifier.classify_many(word_feats("fried chip good and crunchy dig thattaco tropical omg so eyeopening"))

