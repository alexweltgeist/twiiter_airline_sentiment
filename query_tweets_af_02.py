# -*- coding: utf-8 -*-
"""
Bag of words approach on airfrance tweets

Created on Mon Dec 19 08:49:15 2020
Version 02
@author: alexander furrer
"""

# Import required packages
import re
import operator
import pandas as pd
from collections import defaultdict
import nltk
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords

# Load stopwords and filepath into variables
nltk.download('stopwords')
myStopwords = set(stopwords.words('english'))
path = 'C:/Users/alex/Documents/Data_Science_local/CAS_Information_Engineering/C_Information_Retrieval/Project/'

# Prep and filter raw-data, convert csv in txt
def extractText(filename):
    df_tweets = pd.read_csv(path + filename)
    df_tweets.loc[:, 'tweet_text'].to_csv(path + 'tweets.txt', 'w', index=0, header=0)

# Read text corpus in memory
def readTextCorpus(filename):
	tweetlist = ''
	with open(filename, 'r', encoding = 'utf-8') as f:
		tweetlist = f.readlines()
	return tweetlist

# Create list of list of Tweet-tokens (no Stoppwords, with Stemming, MULTIPLE tokens)
def listOfList(tweetlist):
	stemmer = SnowballStemmer('english')
	tweet_lol = []
	for tweet in tweetlist:
		tokenlist = []
		tokens = tweet.split(' ')
		for token in tokens:
			cleanToken = re.sub(r'\W+', '', token).lower()
			if cleanToken not in myStopwords:
				stemToken = stemmer.stem(cleanToken)
				tokenlist.append(stemToken)
		tweet_lol.append(tokenlist)
	return tweet_lol

# Create list of list of Tweet-tokens (no Stoppwords, with Stemming, UNIQUE tokens)
def listOfListUnique(tweetlist):
	stemmer = SnowballStemmer('english')
	tweet_lol_u = []
	for tweet in tweetlist:
		tokenlist = []
		tokens = tweet.split(' ')
		for token in tokens:
			cleanToken = re.sub(r'\W+', '', token).lower()
			if cleanToken not in myStopwords:
				stemToken = stemmer.stem(cleanToken)
				if stemToken not in tokenlist:
					tokenlist.append(stemToken)
		tweet_lol_u.append(tokenlist)
	return tweet_lol_u

# Create list of tokens from query (no Stoppwords, with Stemming, unique tokens)
def listUnique(query):
    stemmer = SnowballStemmer('english')
    tokenlist =[]
    tokens = query.split(' ')
    for token in tokens:
        cleanToken = re.sub(r'\W+', '', token).lower()
        if cleanToken not in myStopwords:
            stemToken = stemmer.stem(cleanToken)
            if stemToken not in tokenlist:
                tokenlist.append(stemToken)
    return tokenlist

# Dictionary of all tokens with Tweet-occurence per tweet (inverted index)
def createInvertedIndex(tweet_lol):
    index = defaultdict(list)
    for i, tweet in enumerate(tweet_lol):
        for token in tweet:
            index[token].append(i)
    return index

# Print all Tweets that contain a specific queryword (no ranking)
def printAllTweets(queryword):
    hits = invertedindex[queryword]
    for hit in hits:
        print(tweetlist[hit])
#        print(tweet_lol[hit])

# Calculate document score based on number of matched query term (number of hits)
def score1(tweet_lol, query):
    scores = []
    qterms = listUnique(query)
    for tweet in tweet_lol:
        score = 0
        for qterm in qterms:
            if qterm in tweet:
                score += 1
        scores.append(score)
    return scores

# Calculate document score based on frequency of query terms in document (number of occurence)
def score2(tweet_lol, query):
    scores = []
    qterms = listUnique(query)
    for tweet in tweet_lol:
        score = 0
        for qterm in qterms:
            score += tweet.count(qterm)
        scores.append(score)
    return scores

# Calculate document score based on position of query terms in document (earlier is better)
def score3(tweet_lol, query):
    scores = []
    qterms = listUnique(query)
    for tweet in tweet_lol:
        score = 0
        for qterm in qterms:
            try:
                position = tweet.index(qterm)
                score = max(int(5.1 - ((position + 1)/6)), score)      
            except ValueError:
                pass
        scores.append(score)
    return scores

# Create a blended score with sum of score 1 to 3
def scoreCombined(tweet_lol, query):
    score_dims = [score1(tweet_lol, query), score2(tweet_lol, query), score3(tweet_lol, query)]
    final_scores = {}
    for i, tweet in enumerate(tweet_lol):
        final_scores[i] = score_dims[0][i] + score_dims[1][i] + score_dims[2][i]
    return final_scores

# Apply scores and select top-n tweets
def evaluateScores(scores, tweetlist, N):
    topnitems = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)[0:N]
    result = ''
    for item in topnitems:
        if item[1] > 0.0:
            result = result + ' --> ' + str(item[1]) + ' Points: ' + tweetlist[item[0]].strip() + '\n\n'
    return result

def answer(query):
    if len(evaluateScores(scoreCombined(tweet_lol, query), tweetlist, 20)) > 0:
        print(query + '\n\n {}'.format(evaluateScores(scoreCombined(tweet_lol, query), tweetlist, 20)))
    else:
        print('\n Cound not find any tweets around this topic.')    

# Process raw data to prepare for queries
extractText('airlineTweetsSentiments.csv')
tweetlist = readTextCorpus(path + 'tweets.txt')
tweet_lol = listOfList(tweetlist)
tweet_lol_u = listOfListUnique(tweetlist)
invertedindex = createInvertedIndex(tweet_lol_u)   


# Main
answer(input('What do you want to search for in the airfrance tweets:  '))
# query = 'what the fuck is this all about airfrance?'
# answer(query)

