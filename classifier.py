import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
import nltk.classify
from sklearn.svm import LinearSVC


 
def word_feats(words):
    return dict([(word, True) for word in words])
 
negids = movie_reviews.fileids('neg')
posids = movie_reviews.fileids('pos')
 
negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]
 
negcutoff = len(negfeats)*3/4
poscutoff = len(posfeats)*3/4
 
trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]


classifier = nltk.classify.NaiveBayesClassifier.train(trainfeats)
print sorted(classifier.labels())
print classifier.classify_many(word_feats("Fish is excellent"))






#classifier = nltk.classify.SklearnClassifier(LinearSVC())

#print 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))
#classifier.train(trainfeats)
#print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)

#print classifier.classify_many(word_feats("Fish is excellent"))
#classifier.show_most_informative_features()