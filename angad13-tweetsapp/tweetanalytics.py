#!/usr/bin/env python
import tweepy as tw
import collections
import pandas as pd
import re
import itertools
import nltk
from nltk.corpus import stopwords
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

consumer_key= 'nxNhgFKyzWyS2LB07taUZxLJJ'
consumer_secret= 'xf61HgZ7SDdwO6tK7vhEPg9ACmc9mupNjApaOxjefTpS1C1lXZ'
access_token= '1152679212953870339-DfzTeuJR9KWiWEn18y6tuSIUK0QABo'
access_token_secret= 'AMMmM84jbAvEKQbYR8VZPsIJ6kunDw7PZ8FuKrUahJEwl'

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

# Collect tweets
def remove_url(txt):
    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())

def get_tweet_data(search_words):	
	log.debug("In get_tweet_data() Search word = "+search_words +" "+ datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
	filtered_search = search_words + " -filter:retweets"

	#initialize a list to hold all the tweepy Tweets
	batchalltweets = []
	#initialize a list to hold text from all the tweepy Tweets
	all_tweets = []

	#make initial request for most recent tweets (100 is the maximum allowed count)
	try:				   
		tweets = api.search(q=filtered_search,
						   lang="en",
						   count=100,
						   since='2018-04-23')
	except:
		tweets = []
		log.error("api.search() returned an error")
		
	log.debug("api.search returned at "+ datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
	#save most recent tweets
	batchalltweets.extend(tweets)
	if len(batchalltweets) > 0:
		#save the id of the oldest tweet less one
		oldest = batchalltweets[-1].id - 1
		log.info("len(tweets) = {}".format(len(tweets)))
		
		counter = 1
		log.debug("Starting to grab 1k tweets at "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))	

		#keep grabbing tweets until you retrieve 1K tweets or there are no tweets left to grab(whichever lesser)		
		while counter<10 and len(tweets) > 0:
			log.info("counter =  {}  len = {}".format(counter, len(tweets)))
			log.debug("getting tweets before %s" % (oldest))
			
			#retrieve subsequent 100 tweets within the loop using max_id param to prevent duplicates
			try:
				tweets = api.search(q=filtered_search,
							   lang="en",
							   count=100,
							   since='2018-04-23',max_id=oldest)		
			except:
				tweets = []
				log.error("api.search() returned an error")
				
			#save most recent tweets
			batchalltweets.extend(tweets)
			
			#update the id of the oldest tweet less one
			oldest = batchalltweets[-1].id - 1		
			log.info("...%s tweets downloaded so far" % (len(batchalltweets)))
			counter = counter+1
			
		log.debug("Finished grabbing the tweets at "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

		all_tweets = [tweet.text for tweet in batchalltweets]		
		log.debug("Finished retrieving tweet text at "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
	
	return get_tweet_analytics(all_tweets)
	
def get_tweet_analytics(all_tweets):
	if len(all_tweets) == 0:
		log.info("No tweets found. Returning None.")
		return None

	all_tweets_no_urls = [remove_url(tweet) for tweet in all_tweets]
	log.debug("Tweet URLS removed at "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
	log.debug(all_tweets_no_urls[:5])
	 
	# Create a list of lists containing lowercase words for each tweet
	words_in_tweet = [tweet.lower().split() for tweet in all_tweets_no_urls]

	# List of all words across tweets
	all_words_no_urls = list(itertools.chain(*words_in_tweet))

	nltk.download('stopwords')
	stop_words = set(stopwords.words('english'))

	tweets_nostopwords = [[word for word in tweet_words if not word in stop_words]
				  for tweet_words in words_in_tweet]

	all_words_nostopwords = list(itertools.chain(*tweets_nostopwords))

	counts_nostopwords = collections.Counter(all_words_nostopwords)

	clean_tweets_nostopwords = pd.DataFrame(counts_nostopwords.most_common(30),
								 columns=['words', 'count'])
	log.debug("Cleaned up tweets at "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
	log.debug(clean_tweets_nostopwords)
	return clean_tweets_nostopwords

if __name__ == '__main__':
	#pass in the keyword you want to download - Dummy function for standalone testing only
	get_tweet_data("modi")
