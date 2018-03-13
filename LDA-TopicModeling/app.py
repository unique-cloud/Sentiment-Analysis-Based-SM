# Basic Flask application to provide access to various textrank functions
# through a REST API

from flask import Flask,abort,jsonify,make_response,request, url_for
import logging
import gensim.summarization as genism
import keyphrase_textrank as kptr
import textacyutility as txtutility
import keyphrase_index as kpindex
import threading
import json
import datetime
import zulu
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

app = Flask(__name__,static_folder=None)


#to keep track of status for respective session
indexStatusCheckMap = {}



def setFlag(id,status = False):
    indexStatusCheckMap[id] = status


def getFlag(id):
    return indexStatusCheckMap[id]

#to launch a separate thread for creating index
#TODO add status for respective sessionID
class myThread (threading.Thread):
    def __init__(self, sessionID,restEndPoint,sourceType,destinationType,query):
        threading.Thread.__init__(self)
        self.threadID = sessionID
        self.rest = restEndPoint
        self.sourceType = sourceType
        self.destinationType = destinationType
        self.query = query

    def run(self):
        logging.info("thread started, query recieved: %s",str(self.query))
        sessionID = self.threadID
        #setFlag(sessionID)
        
        allJSONObjects = kpindex.getJSONObjectsFromElasticSearch(self.rest, self.sourceType,self.threadID,self.query)
        logging.info("data retrieved from Elastic search creating index now")
        
        textData = kpindex.getAllTextData(allJSONObjects)
        indexes,totalDistinctKeywords = kpindex.getBookBackIndexes(textData,allJSONObjects)
        logging.info("Index creation done")
        documentData,totalDocuments = kpindex.getTitles(allJSONObjects)
        currentDateZulu = zulu.now()
        date = zulu.parse(currentDateZulu).isoformat()#datetime.datetime.now().isoformat()
        
        conceptData,totalConcepts=kpindex.getConcepts(allJSONObjects)
        metadata = {"totalDocuments":totalDocuments,"dateCreated":date,"totalKeywords":totalDistinctKeywords,"totalConcepts":totalConcepts} 
        url = self.rest + self.destinationType +"/"+sessionID
        insertsuccess = kpindex.insertIntoElasticSearch(indexes,documentData,conceptData,metadata,url)
        setFlag(sessionID,True)
        



@app.route('/')
def index():
    """Lists the available REST endpoints for the application.

    Args:
        none

    Returns:
        A json array containing a JSON array indexed at "endPoints".
        Each element in the array contains a JSON object with ...

	Example:
        {
          "code": 200,
          "endPoints": [
          {
            "methods": "GET,OPTIONS,HEAD",
            "rule": "/"
          },
          {
            "methods": "OPTIONS,POST",
            "rule": "/textrank/keyphrase/<float:r>"
          }
          ]
        }

    Raises:
        None
    """
    routes = []
    for rule in app.url_map.iter_rules():
        myRule = {}
        myRule["rule"] = rule.rule
        myRule["methods"] = ",".join(list(rule.methods))
        #myRule["function"] = rule.endpoint
        routes.append(myRule)

    return jsonify(code=200, endPoints=routes)

@app.route('/textrank/summary/<float:r>',methods=['POST'])
def getSummary(r):
    """ Summarizes text based upon gensim's implementation of textrank

    Args:
        r - what % of the text should be provided as a summary
        post data - json object with a string attribute called "text"
                    which contains the text to be summarized.

    Returns:
        A json object with a single element "summary" that is a json
        array of the sentences to be used as the summary.  Each element
        is a string

        Example:
        {
          "summary": [
             "sentence 1",
             "sentence 2",
             ...
             "sentence n"
          ]
        }

    Raises:
        None
    """
    contentJSON = request.json
    text = contentJSON['text']
    summary = genism.summarize(text, split=True,ratio = r);
    return jsonify({'summary':summary});

#keyphrase extraction
@app.route('/textrank/keyphrase/<float:r>',methods=['POST'])
def getKeyphrases(r):
    """ Retrieves the top keyphrases

    Args:
        r - what % of the top keywords should be provided.
            The 1.0 would return all keywords
        post data - json object with a string attribute called "text"
                    which contains the text to have the keywords returned.

    Returns:
        A json object with a single element "keywords" that is a json
        array of

        Example:
        {
          "keyphrase": [
            {
              "score": 0.30112727244135246,
              "phrase": "trump"
            },
            {
              "score": 0.2880290370874553,
              "phrase": "clinton"
            }
          ]
        }
    Raises:
        None
    """

    text = request.get_json(silent = True)['text']
    keyphrase = kptr.score_keyphrases_by_textrank(text,r)
    #print(keyphrase)
    result = [{ "phrase": k[0], "score": k[1] } for k in keyphrase]
    return jsonify({'keyphrase': result});

@app.route('/textrank/keyword/<float:r>',methods=['POST'])
def getKeyWords(r):
    """ Retrieves the top keywords based upon gensim's implementation of textrank
    By default, words are lemmatized to reduce duplicates.

    Args:
        r - what % of the top keywords should be provided.
            The 1.0 would return all keywords
        post data - json object with a string attribute called "text"
                    which contains the text to have the keywords returned.

    Returns:
        A json object with a single element "keywords" that is a json
        array of

        Example:
        {
          "keyword": [
            {
              "score": 0.30112727244135246,
              "word": "trump"
            },
            {
              "score": 0.2880290370874553,
              "word": "clinton"
            }
	  ]
	}
    Raises:
        None
    """

    text = request.get_json(silent = True)['text']
    keywordlist = genism.keywords(text,ratio = r,scores=True,split=True,lemmatize=True)
    result = [{ "word": str(k[0]), "score": k[1][0] } for k in keywordlist]
    return jsonify({'keywords':result});

@app.route('/textrank/sgrank/<int:num>',methods=['POST'])
def getSgrank(num):
    text = request.get_json(silent = True)['text']
    doc = txtutility.textacy.Doc(text)
    resultlist = txtutility.mySgRank(doc,n_keyterms=num)
    result = [(str(k[0]),k[1]) for k in resultlist]
    return jsonify({'KeyWords by Sgrank':result});

@app.route('/textrank/index',methods=['POST'])
def createAndStoreIndexes():
    data =  json.loads(request.data.decode("utf-8"))
    sessionID = data["sessionID"]
    setFlag(str(sessionID), False) # setting status to false
    restEndPoint = data["urlAndIndex"]
    sourceType = data["type"]
    destinationType = "discoveryIndex"
    query = data["query"]
    #url = str(elasticServer)+str(indexES)+"/"+str(typeES)+"/"+str(sessionID)+"/_create"
    createIndexThread = myThread(sessionID,restEndPoint,sourceType,destinationType,query)
    createIndexThread.start()
    
    return jsonify({"status":"creating"})


@app.route('/textrank/index/status/<id>',methods=['GET'])
def checkCreateIndexStatus(id):

    if str(id) in indexStatusCheckMap.keys():
        indexCreationStatus = getFlag(id)
    else:
        indexCreationStatus = False

    return jsonify({"status":str(indexCreationStatus)})

@app.route('/textrank/index/timeseries',methods=['POST'])
def createTimeSeries():
    data =  json.loads(request.data.decode("utf-8"))
    startTime = data['startTime']
    textData = data['text']
    res = kpindex.createTimeSeries(textData,startTime)

    return jsonify(res)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
