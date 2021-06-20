# -*- coding: utf-8 -*-
"""
Count most used word in airfrance tweets

Created on Mon Dec 19 08:49:15 2020
Version 02
@author: alexander furrer
"""

# Import required packages
import re
import operator
import pandas as pd
import nltk
from nltk.corpus import stopwords

# Load stopwords and filepath into variables
nltk.download('stopwords')
myStopwords = list(stopwords.words('english'))
specList = ['airfrance', 'air', 'france', 'flight', '', 'us', '1', '2', '3']
myStopwords = set(myStopwords + specList)

path = 'C:/Users/alex/Documents/Data_Science_local/CAS_Information_Engineering/C_Information_Retrieval/Project/'

# Prep and filter raw-data, convert csv in txt
def getNegativeTweets(filename):
    df_tweets = pd.read_csv(path + filename)
    df_tweets_neg = df_tweets.loc[df_tweets['tweet_sentiment_value'] == 0]
    df_tweets_neg.loc[:, 'tweet_text'].to_csv(path + 'neg_tweets.txt', 'w', index=0, header=0)

def getPositiveTweets(filename):
    df_tweets = pd.read_csv(path + filename)
    df_tweets_pos = df_tweets.loc[df_tweets['tweet_sentiment_value'] == 2]
    df_tweets_pos.loc[:, 'tweet_text'].to_csv(path + 'pos_tweets.txt', 'w', index=0, header=0)

def getNeutralTweets(filename):
    df_tweets = pd.read_csv(path + filename)
    df_tweets_nwt = df_tweets.loc[df_tweets['tweet_sentiment_value'] == 1]
    df_tweets_nwt.loc[:, 'tweet_text'].to_csv(path + 'nwt_tweets.txt', 'w', index=0, header=0)

# Read text corpus in memory
def readTextCorpus(filename):
	tweetlist = ''
	with open(filename, 'r', encoding = 'utf-8') as f:
		tweetlist = f.readlines()
	return tweetlist

# Create list of list of Tweet-tokens (no Stoppwords, no Stemming, MULTIPLE tokens)
def listOfList(tweetlist):
	tweet_lol = []
	for tweet in tweetlist:
		tokenlist = []
		tokens = tweet.split(' ')
		for token in tokens:
			cleanToken = re.sub(r'\W+', '', token).lower()
			if cleanToken not in myStopwords:
				tokenlist.append(cleanToken)
		tweet_lol.append(tokenlist)
	return tweet_lol

def topNWords(tweet_lol, N):
    myDict = {}
    for tweet in tweet_lol:
        for token in tweet:
            if token in myDict and token not in myStopwords:
                myDict[token] = myDict[token] + 1
            else:
                myDict[token] = 1
    top10 = sorted(myDict.items(), key=operator.itemgetter(1), reverse=True)[:N]
#    return myDict
    return top10

def printNice(myDict, title):
    myList = list(myDict)
    print('\n Most used word in', title, 'tweets.\n')
    for item in myList:
        print(item[1], ' times: ', item[0])

# Process raw data to prepare for queries
getNegativeTweets('airlineTweetsSentiments.csv')
getPositiveTweets('airlineTweetsSentiments.csv')
getNeutralTweets('airlineTweetsSentiments.csv')
neg_tweet_lol = listOfList(readTextCorpus(path + 'neg_tweets.txt'))
pos_tweet_lol = listOfList(readTextCorpus(path + 'pos_tweets.txt'))
nwt_tweet_lol = listOfList(readTextCorpus(path + 'nwt_tweets.txt'))

# Main
printNice(topNWords(neg_tweet_lol, 20), 'negative')
printNice(topNWords(pos_tweet_lol, 20), 'positive')
printNice(topNWords(nwt_tweet_lol, 20), 'neutral')
