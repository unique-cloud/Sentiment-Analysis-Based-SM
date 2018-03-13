from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import summarizer as sm
import gensim.summarization as gensim
import lexrank as lx
import textacyutility as txtutility
import re
import operator



def get_content(filepath):
	print "checkpoint"
	file = BeautifulSoup(open(filepath),"lxml")
	content = file.find("sentences")
	fulltext = content.get_text()
	return fulltext

def get_keywords_from_summarizer(fulltext):
	scores = sm.score_keyphrases_by_textrank(unicode(fulltext))
	return scores

def get_summary_from_gensim(fulltext,r = 0.02):
	summary = gensim.summarize(fulltext,r)
	return summary

def get_keyphrase_from_gensim(fulltext,r = 0.02):
	keywords = gensim.keywords(fulltext)
	return keywords



def get_summary_from_lexrank(fulltext):
	LANGUAGE = "english"
	SENTENCES_COUNT = 10
	stemmer = lx.Stemmer(LANGUAGE)
	summarizer = lx.Summarizer(stemmer)
	summarizer.stop_words = lx.get_stop_words(LANGUAGE)
	file = open("keysentences1.txt",'w')
	file.write(text)
	parser = lx.PlaintextParser.from_file("keysentences1.txt", lx.Tokenizer(LANGUAGE))
	sentences = []
	for sentence in summarizer(parser.document, 3):
		sentences.append(sentence)
	return sentences


def get_keyphrase_from_sgrank(fulltext,n=10):
	doc = txtutility.textacy.Doc(unicode(fulltext))
	resultlist = txtutility.mySgRank(doc,n_keyterms=15)
	result = [(str(k[0]),k[1]) for k in resultlist]
	return result

def sentence_extractor(file_path, key_words_scores):
   y = BeautifulSoup(open(file_path), "lxml")
   a = y.findAll("sentences")
   content = [x.get_text() for x in a]
   text = "".join(content)
   
   remove_words = []
   key_words = dict(key_words_scores)

   for word1 in key_words.keys():
       for word2 in key_words.keys():
           if word1 != word2:
               if word1 in word2:
                   remove_words.append(word1)

   for key in key_words.keys():
       if key in remove_words:
           del key_words[key]

   sentences = {}

   for key_word in key_words:
       phrase = '.*'+key_word+'.*'
       occurrences_pos = [(a.start(), a.end()) for a in list(re.finditer(phrase, text.lower()))]
       for (start,end) in occurrences_pos:
           if text[start:end+1] not in sentences.keys():
               sentences[text[start:end+1]] = key_words[key_word]
           else:
               sentences[text[start:end+1]] = sentences[text[start:end+1]]+key_words[key_word]

   sentences = sorted(sentences.items(), key=operator.itemgetter(1))

   return [sentence[0] for sentence in sentences]

def get_phrases_from_summary(list_of_key,summary):

   key_word = [word[0] for word in list_of_key]
   summary_list = summary.split()

   summary_list = [word.lower() for word in summary_list if word.lower() not in stopwords.words('english')]

   phrases_in_summary = []

   for word in list_of_key:
       temp=word[0]
       if len(temp.split(' ')) > 1:
           temp = temp.split(' ')[0]
       if temp in summary_list:
           index_of_temp = summary_list.index(temp)
           phrases_in_summary.append(' '.join(summary_list[index_of_temp-2:index_of_temp+2]))




'''

filepath = "holdoutHalf-catchphrasesOUT/06_1.xml"
text = get_content(filepath)
keyphraselist = get_keywords_from_summarizer(text)

rs = {}
for x in keyphraselist:
    #print(x[0])
    word = x[0]
    if(len(word.split()) > 1):
    	if word not in rs.keys():
    		rs[word] = x[1]
rs = rs.items()


sentencelist = sentence_extractor(filepath,rs)

summarygensim = get_summary_from_gensim("".join(sentencelist))
print summarygensim
print ""
summarylex = get_summary_from_lexrank(text)

print summarylex
print ""

keyphrasesgenism = get_keyphrase_from_sgrank(summarygensim)

for x in keyphrasesgenism:
	print x

keyphraseslex = get_keyphrase_from_sgrank(summarylex)
print ""
for x in keyphraseslex:
	print x
'''

