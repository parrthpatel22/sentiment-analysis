import re
import string
import numpy as np
import pandas as pd
import nltk
nltk.download('stopwords')
from nltk.stem import PorterStemmer 
from nltk.corpus import stopwords 
import gensim
from gensim import corpora
import itertools
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib import pyplot
from sklearn.decomposition import PCA
from sklearn.preprocessing import LabelEncoder
import keras
from keras.models import Sequential
from keras.callbacks import ReduceLROnPlateau, EarlyStopping
from keras.layers import Activation, Dense, Dropout, Embedding,  LSTM
from tensorflow.keras import layers

import twitter
from datetime import date
import datetime


from flask import Flask, redirect, url_for, request
from flask_cors import CORS, cross_origin
from flask_ngrok import run_with_ngrok
app = Flask(__name__)
# cors = CORS(app)
#run_with_ngrok(app)
app.config['CORS_HEADERS'] = 'Content-Type'


model = gensim.models.KeyedVectors.load_word2vec_format('twitter-word2Vecmodel.bin', binary = True)
print(gensim.__version__)
vocabulary = list(model.key_to_index)
print(len(vocabulary))
tweetModel = keras.models.load_model('tweetFolder-II')

words = []
for i in range(0,len(vocabulary)):
  words.append(vocabulary[i])
print(len(words))
embedding_matrix = np.zeros((len(vocabulary)+1, 100))
embedding_matrix[0] = np.zeros(100)
i = 1
for word in words:
  embedding_matrix[i] = model[word]
  i = i+1
print(embedding_matrix.shape)
embedding_layer = Embedding(len(vocabulary)+1, 100, weights=[embedding_matrix], input_length=50, trainable = False)



def predictTweet(tweet):
  tweet = re.sub('@[^\s]+','',tweet)
  tweet = re.sub('http[^\s]+','',tweet)
  tweet = tweet.translate(str.maketrans('', '', string.punctuation))
  tweet = tweet.lower()
  tweet = re.sub(" \d+", "", tweet)
  tweet = tweet.split()
  stop_words = set(stopwords.words('english')) 
  stop_words.add("im")
  stop_words.remove("no")
  stop_words.remove("against")
  stop_words.remove("not")
  stop_words.remove("don")
  filtered_tweet = []
  for word in tweet:
    if(word not in stop_words):
      filtered_tweet.append(word)
  if(len(tweet)>15):
    tweet = filtered_tweet[:15]
  #print(tweet)
  filtered_tweet = []
  ps = PorterStemmer() 
  for word in tweet:
    filtered_tweet.append(ps.stem(word))
  tweet = filtered_tweet
  #tweet = ['nahi', 'khate', 'tum', 'jaise', 'fir', 'se', 'rote', 'ki', 'modi', 'dushmani', 'badha', 'raha', 'hai', 'surgical']
  ids = []
  i = 0
  for i in range(0,len(tweet)):
    if(tweet[i] in words):
      id = words.index(tweet[i])+1
      if(id>42469):
        ids.append(0)
      else:
        ids.append(words.index(tweet[i]) + 1)
    else:
      ids.append(0)
  for i in range(len(tweet),50):
      ids.append(0)
  test = []
  test.append(ids)
  x = np.array(test)
  #print(x)
  result = tweetModel.predict(x)
  if (result[0][0] < 0.5):
    return (str(result[0][0]), "Negative")
  else:
    return (str(result[0][0]), "Positive")

# print(predictTweet("its was bad"))
# print(predictTweet("at first it was good, then bad, then good, in conclusion, it was bad"))
# print(predictTweet("initially i thought it would be a great dish ..but i found it to be the worst dish I have ever eaten"))


def getDateFromStr(d):
  date_object = datetime.datetime.strptime(d, '%a %b %d %X %z %Y').date()
  return date_object

def getTweets(word):
  consumer_key= ''
  consumer_secret= ''
  access_token= ''
  access_token_secret= ''
  api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token,
                  access_token_secret=access_token_secret)
  tweets = {}
  for i in range(-1,6):
    until = date.today()-datetime.timedelta(i)
    until_date = until
    until_str = str(until)
    results = api.GetSearch(
    raw_query="q="+word+"%20until%3A"+until_str+"&count=100-filter%3Areplies")
    tweets[str(until_date- datetime.timedelta(1))] = []
    for t in results:
      if(getDateFromStr(t.created_at) == until_date- datetime.timedelta(1)):
        tweets[str(until_date- datetime.timedelta(1))].append(t.text.replace("\n",""))
  return tweets


#print(getTweets("modi")[str(date.today())])

    
def getSentimentTweets(keyword):
    tweets = getTweets(keyword)
    sentimentTweets = {}    
    for d in tweets:
        sentimentTweets[d] = {'pos': [], 'neg': []}
        for tweet in tweets[d]:
            sentiment = predictTweet(tweet)
            if (sentiment[1] == "Positive"):
                sentimentTweets[d]['pos'].append(tweet)
            else:
                sentimentTweets[d]['neg'].append(tweet)
        sentimentTweets[d]['pos_count'] = len(sentimentTweets[d]['pos'])
        sentimentTweets[d]['neg_count'] = len(sentimentTweets[d]['neg'])
        sentimentTweets[d]['total_count'] = len(sentimentTweets[d]['pos']) + len(sentimentTweets[d]['neg'])
    for d in tweets:
        print(d,sentimentTweets[d]['pos_count'],sentimentTweets[d]['neg_count'])
    return sentimentTweets

# print("Ronaldo")
# getSentimentTweets("ronaldo")

#print("modi")
#getSentimentTweets("modi")
            
        
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response


@app.route('/analyse',methods = ['POST'])
def analyse():
    return getSentimentTweets(request.json['word'])


@app.route('/sentiments',methods = ['POST'])
def getSentiments():
    result = {}
    for i in request.json['words']:
        result[i] = getSentimentTweets(i)
    return result



@app.route('/sentiment',methods = ['POST'])
def getsentiment():
    print(request.json)
    sentence = request.json['sentence']
    print(predictTweet(sentence))
    return {"sentiment" :predictTweet(sentence)}

@app.route('/singlelinesentiment',methods = ['POST'])
def getSingleSentiment():
    sentence = str(request.args['sentence'])
    print(predictTweet(sentence))
    return {"sentiment" :predictTweet(sentence)}


app.run(host ='0.0.0.0', port = 5000, debug = True)

