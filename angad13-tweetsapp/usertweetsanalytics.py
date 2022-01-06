#!/usr/bin/env python

import tweepy as tweepy
from tweetanalytics import get_tweet_analytics
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

consumer_key= 'nxNhgFKyzWyS2LB07taUZxLJJ'
consumer_secret= 'xf61HgZ7SDdwO6tK7vhEPg9ACmc9mupNjApaOxjefTpS1C1lXZ'
access_token= '1152679212953870339-DfzTeuJR9KWiWEn18y6tuSIUK0QABo'
access_token_secret= 'AMMmM84jbAvEKQbYR8VZPsIJ6kunDw7PZ8FuKrUahJEwl'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)


def get_all_user_tweets(screen_name):
	log.debug("In get_all_user_tweets() screen name : {}".format(screen_name)) 
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#initialize a list to hold text from all the tweepy Tweets
	outtweets = []
	
	try:
		#make initial request for most recent tweets (200 is the maximum allowed count)
		new_tweets = api.user_timeline(screen_name = screen_name,count=200)	
	except:
		new_tweets = []
		log.error("api.user_timeline() returned an error")
		
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	if len(alltweets) > 0:
		#save the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		log.info("len(new_tweets) = {}".format(len(new_tweets)))		
		
		counter = 1
		log.debug("Starting to grab 1K tweets for the user handle "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))	
		
		#keep grabbing tweets until you retrieve 1K tweets or there are no tweets left to grab(whichever lesser)
		while counter<5 and len(new_tweets) > 0:
			log.debug("getting tweets before %s" % (oldest))
			
			try:
				#retrieve subsequent 200 tweets within the loop using max_id param to prevent duplicates
				new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
			except:
				new_tweets = []
				log.error("api.user_timeline() returned an error")
				
			log.info("len(new_tweets) = {}".format(len(new_tweets)))
			#save most recent tweets
			alltweets.extend(new_tweets)
			
			#update the id of the oldest tweet less one
			oldest = alltweets[-1].id - 1		
			log.info("...%s tweets downloaded so far" % (len(alltweets)))	
			counter = counter+1
		
		log.debug("Finished grabbing 1K tweets for the user handle "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
		outtweets = [tweet.text for tweet in alltweets]
		log.debug("EXtracted text from tweets for the user handle "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
	return get_tweet_analytics(outtweets)

if __name__ == '__main__':
	#pass in the username of the account you want to download - Dummy function for standalone testing only
	get_all_user_tweets("narendramodi")
