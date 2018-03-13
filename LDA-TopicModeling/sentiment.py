import sys
import collections
import sklearn.naive_bayes
import sklearn.linear_model
import nltk
import random
from collections import Counter
import numpy as np

random.seed(0)
from gensim.models.doc2vec import LabeledSentence, Doc2Vec
nltk.download("stopwords")          # Download the stop words from nltk


# User input path to the train-pos.txt, train-neg.txt, test-pos.txt, and test-neg.txt datasets
if len(sys.argv) != 3:
    print "python sentiment.py <path_to_data> <0|1>"
    print "0 = NLP, 1 = Doc2Vec"
    exit(1)
path_to_data = sys.argv[1]
method = int(sys.argv[2])



def main():
    train_pos, train_neg, test_pos, test_neg = load_data(path_to_data)
    
    if method == 0:
        train_pos_vec, train_neg_vec, test_pos_vec, test_neg_vec = feature_vecs_NLP(train_pos, train_neg, test_pos, test_neg)
        nb_model, lr_model = build_models_NLP(train_pos_vec, train_neg_vec)
    if method == 1:
        train_pos_vec, train_neg_vec, test_pos_vec, test_neg_vec = feature_vecs_DOC(train_pos, train_neg, test_pos, test_neg)
        nb_model, lr_model = build_models_DOC(train_pos_vec, train_neg_vec)
    print "Naive Bayes"
    print "-----------"
    evaluate_model(nb_model, test_pos_vec, test_neg_vec, True)
    print ""
    print "Logistic Regression"
    print "-------------------"
    evaluate_model(lr_model, test_pos_vec, test_neg_vec, True)



def load_data(path_to_dir):
    """
    Loads the train and test set into four different lists.
    """
    train_pos = []
    train_neg = []
    test_pos = []
    test_neg = []
    with open(path_to_dir+"train-pos.txt", "r") as f:
        for i,line in enumerate(f):
            words = [w.lower() for w in line.strip().split() if len(w)>=3]
            train_pos.append(words)
    with open(path_to_dir+"train-neg.txt", "r") as f:
        for line in f:
            words = [w.lower() for w in line.strip().split() if len(w)>=3]
            train_neg.append(words)
    with open(path_to_dir+"test-pos.txt", "r") as f:
        for line in f:
            words = [w.lower() for w in line.strip().split() if len(w)>=3]
            test_pos.append(words)
    with open(path_to_dir+"test-neg.txt", "r") as f:
        for line in f:
            words = [w.lower() for w in line.strip().split() if len(w)>=3]
            test_neg.append(words)

    return train_pos, train_neg, test_pos, test_neg



def feature_vecs_NLP(train_pos, train_neg, test_pos, test_neg):
    """
    Returns the feature vectors for all text in the train and test datasets.
    """
    # English stopwords from nltk
    stopwords = set(nltk.corpus.stopwords.words('english'))

    # Determine a list of words that will be used as features. 
    # This list should have the following properties:
    #   (1) Contains no stop words
    #   (2) Is in at least 1% of the positive texts or 1% of the negative texts
    #   (3) Is in at least twice as many postive texts as negative texts, or vice-versa.
    # YOUR CODE HERE

    # Using the above words as features, construct binary vectors for each text in the training and test set.
    # These should be python lists containing 0 and 1 integers.
    # YOUR CODE HERE

    pos_filtered=[set(x)-stopwords for x in train_pos]
    neg_filtered=[set(x)-stopwords for x in train_neg]
    all_pos_list=[x for text in pos_filtered for x in text]
    all_neg_list=[x for text in neg_filtered for x in text]
    pos_dict=Counter(all_pos_list)
    neg_dict=Counter(all_neg_list)
    all_words=list(set(all_pos_list).union(set(all_neg_list)))
    feature_list=[]
    for word in all_words:
    	if (pos_dict[word]>=.01*len(train_pos) or neg_dict[word]>=.01*len(train_neg)) and (pos_dict[word] >= 2*neg_dict[word] or neg_dict[word] >= 2*pos_dict[word]):
    		feature_list.append(word)
    



    train_pos_vec=[[1 if word in text else 0 for word in feature_list] for text in train_pos]
    train_neg_vec=[[1 if word in text else 0 for word in feature_list] for text in train_neg]
    test_pos_vec=[[1 if word in text else 0 for word in feature_list] for text in test_pos]
    test_neg_vec=[[1 if word in text else 0 for word in feature_list] for text in test_neg]




    # Return the four feature vectors
    return train_pos_vec, train_neg_vec, test_pos_vec, test_neg_vec



def feature_vecs_DOC(train_pos, train_neg, test_pos, test_neg):
    """
    Returns the feature vectors for all text in the train and test datasets.
    """
    # Doc2Vec requires LabeledSentence objects as input.
    # Turn the datasets from lists of words to lists of LabeledSentence objects.
    # YOUR CODE HERE
    labeled_train_pos=[]
    labeled_train_neg=[]
    labeled_test_pos=[]
    labeled_test_neg=[]
    i=1
    for text in train_pos:
    	labeled_train_pos.append(LabeledSentence(text, ['TRAIN_POS_'+str(i)]))
    	i=i+1
    i=1
    for text in train_neg:
    	labeled_train_neg.append(LabeledSentence(text, ['TRAIN_NEG_'+str(i)]))
    	i=i+1
    i=1
    for text in test_pos:
    	labeled_test_pos.append(LabeledSentence(text, ['TEST_POS_'+str(i)]))
    	i=i+1
    i=1
    for text in test_neg:
    	labeled_test_neg.append(LabeledSentence(text, ['TEST_NEG_'+str(i)]))
    	i=i+1

    


    # Initialize model
    model = Doc2Vec(min_count=1, window=10, size=100, sample=1e-4, negative=5, workers=4)
    sentences = labeled_train_pos + labeled_train_neg + labeled_test_pos + labeled_test_neg
    model.build_vocab(sentences)
    
    

    # Train the model
    # This may take a bit to run 
    for i in range(5):
        print "Training iteration %d" % (i)
        random.shuffle(sentences)
        model.train(sentences)

    # Use the docvecs function to extract the feature vectors for the training and test data
    # YOUR CODE HERE
    z=1
    train_pos_vec=[]
    train_neg_vec=[]
    test_pos_vec=[]
    test_neg_vec=[]
    for x in labeled_train_pos:
    	train_pos_vec.append(model.docvecs['TRAIN_POS_'+str(z)])
    	z=z+1
    z=1
    for x in labeled_train_neg:
    	train_neg_vec.append(model.docvecs['TRAIN_NEG_'+str(z)])
    	z=z+1
    z=1
    for x in labeled_test_pos:
    	test_pos_vec.append(model.docvecs['TEST_POS_'+str(z)])
    	z=z+1
    z=1
    for x in labeled_test_neg:
    	test_neg_vec.append(model.docvecs['TEST_NEG_'+str(z)])
    	z=z+1
    
    # Return the four feature vectors
    return train_pos_vec, train_neg_vec, test_pos_vec, test_neg_vec



def build_models_NLP(train_pos_vec, train_neg_vec):
    """
    Returns a BernoulliNB and LosticRegression Model that are fit to the training data.
    """
    Y = ["pos"]*len(train_pos_vec) + ["neg"]*len(train_neg_vec)
    
   

    # Use sklearn's BernoulliNB and LogisticRegression functions to fit two models to the training data.
    # For BernoulliNB, use alpha=1.0 and binarize=None
    # For LogisticRegression, pass no parameters
    # YOUR CODE HERE
    X=train_pos_vec+train_neg_vec
    nb_model=sklearn.naive_bayes.BernoulliNB(alpha=1.0, binarize=None)
    nb_model.fit(X,Y)
    lr_model=sklearn.linear_model.LogisticRegression()
    lr_model.fit(X,Y)

    return nb_model, lr_model



def build_models_DOC(train_pos_vec, train_neg_vec):
    """
    Returns a GaussianNB and LosticRegression Model that are fit to the training data.
    """
    Y = ["pos"]*len(train_pos_vec) + ["neg"]*len(train_neg_vec)
    

    # Use sklearn's GaussianNB and LogisticRegression functions to fit two models to the training data.
    # For LogisticRegression, pass no parameters
    # YOUR CODE HERE
    X=train_pos_vec+train_neg_vec
    nb_model=sklearn.naive_bayes.GaussianNB()
    nb_model.fit(X,Y)
    lr_model=sklearn.linear_model.LogisticRegression()
    lr_model.fit(X,Y)

    
    return nb_model, lr_model



def evaluate_model(model, test_pos_vec, test_neg_vec, print_confusion=False):
    """
    Prints the confusion matrix and accuracy of the model.
    """
    # Use the predict function and calculate the true/false positives and true/false negative.
    # YOUR CODE HERE
   
    test_pos_dict= Counter(model.predict(test_pos_vec))
    test_neg_dict= Counter(model.predict(test_neg_vec))
    tp=test_pos_dict['pos']
    fn=test_pos_dict['neg']
    fp=test_neg_dict['pos']
    tn=test_neg_dict['neg']
    accuracy=float(tp+tn)/float(tp+tn+fp+fn)
    
    if print_confusion:
        print "predicted:\tpos\tneg"
        print "actual:"
        print "pos\t\t%d\t%d" % (tp, fn)
        print "neg\t\t%d\t%d" % (fp, tn)
    print "accuracy: %f" % (accuracy)

   

if __name__ == "__main__":
    main()
