#!/usr/bin/python3

# [ (C) January 2018 Hypercoffeedude ] 
# I freely license this script for anyones
# use provided this notice remains intact. 

# The purpose of this script is to reach a total
# for the number of tweets a user has made within
# a certain timeframe. The script, as written,
# totals up all of the tweets from 'realDonaldTrump'
# for the seven days between 1/19 - 1/26 at noon.
# This script should be more accurate than using the
# current method of total tweets on the users page.
# For example, if a user deleted even a few entries
# from months ago, it would currently unfairly affect 
# the outcome of the market. 

import tweepy, datetime, time
from pushover import Client

debug=0

### Twitter API keys/secrets ###
consumer_key = 'yourConsumerKeyHere'
consumer_secret = 'yourConsumerSecretHere'
access_token_key = 'yourAccessTokenHere'
access_token_secret = 'yourAccessTokenSecretHere'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)
api = tweepy.API(auth)

### Choose a target (Twitter username) ###
#target = 'potus'
target = 'realDonaldTrump'

### Go back a number of days ###
days = 7

### Select End date and time eg. 01/26/2018 12:00PM (Timezone=None) ###
end_date = datetime.datetime(2018, 1, 26,12,0,0,0, None)
begin_date = end_date - datetime.timedelta(days=days)

### Prepare list element to hold amount of tweets for each day ###
list_count = [0 for x in range(days)]

### Function to retrieve and process Tweets ###
def get_tweets(api, username):
    count = 0
    while True:
        tweets = tweepy.Cursor(api.user_timeline, id=username).items()
        for tweet in tweets:
            tweetday = end_date-tweet.created_at
            if tweetday.days < days:
                if debug: print(str(tweetday.days)+':'+str(tweet.created_at))
                list_count[tweetday.days]+=1
                count+=1
            else:
                return count
### Call function and receive total number of tweets in time period, (eg. 7 days) ###
count = get_tweets(api, target)

### Format output to console ###
title_text = '@'+target+' Twitter Activity'

print('\n'+title_text+'\n'+('-'*len(title_text)))
print('# of tweets by day:')

for x in range(days):
    print((end_date - datetime.timedelta(days=x)).strftime('%b %d, %Y')+' = '+str(list_count[x]))
total = 0.0

for value in list_count:
    total+=value

message = '\nFrom '+str(end_date.strftime('%b %d, %Y @ %I:%M%p'))+' to '+str(begin_date.strftime('%b %d, %Y @ %I:%M%p'))+', '+'[@'+target+'] has tweeted '+str(count)+' times at an average of '+str(round(total/days, 2))+' tweets per day.\n'
print(message)
