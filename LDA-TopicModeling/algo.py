from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora
from flask import Flask, request, jsonify
import gensim
import json

app = Flask(__name__)

# @ signfies a decorator : way to wrap a function and modifying its behaviour
@app.route('/', methods=['POST'])
def index():
    contentJSON = request.get_json()
    data = {}
    data['micropost_id'] = contentJSON['micropost_id']
    data['content'] = contentJSON['content']
    json_data = json.loads(json.dumps(data))

    #{ params: { micropost_id: integer(same), tags: string array (["test1", "test2", "test3"]) }
    params_data = {}
    params_data['micropost_id'] = json_data['micropost_id']

    #lda
    tokenizer = RegexpTokenizer(r'\w+')

    # create English stop words list
    en_stop = get_stop_words('en')

    # Create p_stemmer of class PorterStemmer
    p_stemmer = PorterStemmer()

    # create sample documents
    doc_a = json_data['content']
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
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=1, id2word=dictionary, passes=1500)
    str_data = json.dumps(ldamodel.print_topics(num_topics=1, num_words=5))
    params_data['response'] = str_data
    #response_json = json.dumps(params_data)
    #response_json = json.loads(response_json)
    return jsonify(params_data)


if __name__ == "__main__":
   app.run(debug=True)