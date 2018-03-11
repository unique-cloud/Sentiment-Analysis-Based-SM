from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
from flask import Flask, request, jsonify
import gensim
import json

app = Flask(__name__)

# @ signfies a decorator : way to wrap a function and modifying its behaviour
@app.route('https://ocean-ncsu.herokuapp.com/combinations', methods=['POST'])
def index():

    #contentJSON = request.JSON
    data = {}
    data['micropost_id'] = 1
    data['content'] = "Lorem ipsum"
    json_data = json.dumps(data)

    params = {}
    params['micropost_id'] = 1
    #{ params: { micropost_id: integer(same), tags: string array (["test1", "test2", "test3"]) }

    #lda
    tokenizer = RegexpTokenizer(r'\w+')

    # create English stop words list
    en_stop = get_stop_words('en')

    # Create p_stemmer of class PorterStemmer
    p_stemmer = PorterStemmer()

    # create sample documents
    doc_a = data['content']
    # compile sample documents into a list
    doc_set = [doc_a]

    # list for tokenized documents in loop
    texts = []

    # loop through document list
    for i in doc_set:
        # clean and tokenize document string
        raw = i.lower()
        tokens = tokenizer.tokenize(raw)

        # remove stop words from tokens
        stopped_tokens = [i for i in tokens if not i in en_stop]

        # stem tokens
        stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]

        # add tokens to list
        texts.append(stemmed_tokens)

    # turn our tokenized documents into a id <-> term dictionary
    dictionary = corpora.Dictionary(texts)

    # convert tokenized documents into a document-term matrix
    corpus = [dictionary.doc2bow(text) for text in texts]

    # generate LDA model
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=2, id2word=dictionary, passes=1500)
    params["tags"] = json.dumps(ldamodel.print_topics(num_topics=2, num_words=3))

    json_data = json.dumps(params)
    return params

'''
@app.route('/profile<username>')
def profile(username):
    return '<h2>Welcome %s</h2>' %username
tokenizer = RegexpTokenizer(r'\w+')

# create English stop words list
en_stop = get_stop_words('en')

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()

# create sample documents
doc_a = "Brocolli is good to eat. My brother likes to eat good brocolli, but not my mother. My mother spends a lot of time driving my brother around to baseball practice. Some health experts suggest that driving may cause increased tension and blood pressure. I often feel pressure to perform well at school, but my mother never seems to drive my brother to do better.Health professionals say that brocolli is good for your health."

# compile sample documents into a list
doc_set = [doc_a]

# list for tokenized documents in loop
texts = []

# loop through document list
for i in doc_set:
    # clean and tokenize document string
    raw = i.lower()
    tokens = tokenizer.tokenize(raw)

    # remove stop words from tokens
    stopped_tokens = [i for i in tokens if not i in en_stop]

    # stem tokens
    stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]

    # add tokens to list
    texts.append(stemmed_tokens)

# turn our tokenized documents into a id <-> term dictionary
dictionary = corpora.Dictionary(texts)

# convert tokenized documents into a document-term matrix
corpus = [dictionary.doc2bow(text) for text in texts]

# generate LDA model
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=2, id2word=dictionary, passes=1500)
print json.dumps(ldamodel.print_topics(num_topics=2, num_words=3))
'''
if __name__ == "__main__":
   app.run(debug=True)