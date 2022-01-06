#!/usr/bin/env python
import tweepy as tw 
import sys
import collections
import pandas as pd
import re
import itertools
import nltk
from nltk.corpus import stopwords
import csv

consumer_key= 'nxNhgFKyzWyS2LB07taUZxLJJ'
consumer_secret= 'xf61HgZ7SDdwO6tK7vhEPg9ACmc9mupNjApaOxjefTpS1C1lXZ'
access_token= '1152679212953870339-DfzTeuJR9KWiWEn18y6tuSIUK0QABo'
access_token_secret= 'AMMmM84jbAvEKQbYR8VZPsIJ6kunDw7PZ8FuKrUahJEwl'

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

# Define the search term and the date_since date as variables
search_words = "persimmonhomes"
date_since = "2018-11-16"

# Collect tweets

tweets = tw.Cursor(api.search,
              q=search_words,
              lang="en",
              since=date_since).items(5)

# Collect a list of tweets
for tweet in tweets:
    print(tweet.text)

#[tweet.text for tweet in tweets]
#   print tweet

new_search = search_words + " -filter:retweets"

tweets = tw.Cursor(api.search, 
                           q=new_search,
                           lang="en",
                           since=date_since).items(5)


users_locs = [[tweet.user.screen_name, tweet.user.location] for tweet in tweets]
print users_locs

tweet_text = pd.DataFrame(data=users_locs, 
                    columns=['user', "location"])

print tweet_text

new_search = search_words + " -filter:retweets"

tweets = tw.Cursor(api.search,
                   q=new_search,
                   lang="en",
                   since='2018-04-23').items(1000)

all_tweets = [tweet.text for tweet in tweets]
print all_tweets[:5]

def remove_url(txt):
    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())

all_tweets_no_urls = [remove_url(tweet) for tweet in all_tweets]
print all_tweets_no_urls[:5]

# Split the words from one tweet into unique elements
print all_tweets_no_urls[0].lower().split()

# Create a list of lists containing lowercase words for each tweet
words_in_tweet = [tweet.lower().split() for tweet in all_tweets_no_urls]
words_in_tweet[:2]


# List of all words across tweets
all_words_no_urls = list(itertools.chain(*words_in_tweet))

# Create counter
counts_no_urls = collections.Counter(all_words_no_urls)

counts_no_urls.most_common(15)

clean_tweets_no_urls = pd.DataFrame(counts_no_urls.most_common(15),
                             columns=['words', 'count'])

print clean_tweets_no_urls.head()

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

tweets_nsw = [[word for word in tweet_words if not word in stop_words]
              for tweet_words in words_in_tweet]

all_words_nsw = list(itertools.chain(*tweets_nsw))

counts_nsw = collections.Counter(all_words_nsw)

counts_nsw.most_common(30)

clean_tweets_nsw = pd.DataFrame(counts_nsw.most_common(30),
                             columns=['words', 'count'])

print clean_tweets_nsw

"""
def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tw.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tw.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print "getting tweets before %s" % (oldest)
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print "...%s tweets downloaded so far" % (len(alltweets))
	
	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
	
	#write the csv	
	with open('%s_tweets.csv' % screen_name, 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(["id","created_at","text"])
		writer.writerows(outtweets)
	
	pass


if __name__ == '__main__':
	#pass in the username of the account you want to download
	get_all_tweets("tim_cook")
	
"""
