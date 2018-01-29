#!/usr/bin/python3
#DEV TEST
import tweepy, datetime, time
from dateutil import relativedelta as rd

##### SETTINGS BEGIN HERE #####
### Choose a target (Twitter username)
twitter_target = 'potus'
#twitter_target = 'realDonaldTrump'

### NOTE: The Twitter API returns dates in UTC (+0000)
### Select begin/end date and time eg. 2018-12-31 12:00:00(24h) Timezone=None)
tweet_date =       datetime.datetime(2018, 1, 26, 12, 0, 0, 0, None)
tweet_date_begin = datetime.datetime(2018, 1, 26, 12, 0, 0, 0, None)
tweet_date_end =   datetime.datetime(2018, 2, 2, 12, 0, 0, 0, None)


##### FUNCTIONS BEGIN HERE #####
### Try to grab Twitter credentials from an external file.
### This file must be updated with your information!
try:
    with open('twitter_keys.txt') as f:
        consumer_key = f.readline().partition('=')[2].strip()
        consumer_secret = f.readline().partition('=')[2].strip()
        access_token_key = f.readline().partition('=')[2].strip()
        access_token_secret = f.readline().partition('=')[2].strip()
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token_key, access_token_secret)
        api = tweepy.API(auth)
except IOError as err:
    print('\n---ERROR!---\n{0}\nMake sure to place this file in the same folder as this script!\n'.format(err))
    raise SystemExit(0)

### Optional Function (Currently Unused) ### 
def get_tweets_by_day(api, date_begin):
    date_since = date_begin.strftime('%Y-%m-%d')
    date_until = (date_begin + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    results = tweepy.Cursor(api.search, q='from:'+twitter_target, since=date_since, until=date_until).items()
    return results

### Main function to retrieve and process Tweets ###
def get_tweets(api, twitter_target, date_begin, date_end):
    while True:
        tweets = tweepy.Cursor(api.user_timeline, id=twitter_target).items(200)
        date_list = []
        for tweet in tweets:
            # Convert 'created_at' (UTC) time to Eastern Standard Time (EST -5 Hours)
            created_at_est = tweet.created_at + datetime.timedelta(hours=-5)
            # Compare tweet time with specified range
            if date_begin < created_at_est < date_end:
                # Add dates of tweets, and tweet text into a list element
                date_list.append([created_at_est, tweet.text[:80]])
            elif date_begin < created_at_est:
                pass
            else:
                break
        # Return a list containing tweet dates and truncted tweet text.
        return date_list

##### MAIN PROGRAM BEGINS HERE #####
# Get list of tweet dates and store them in a list. eg [DATE, "Tweet text"]
date_list = get_tweets(api, twitter_target, tweet_date_begin, tweet_date_end)

# Display formatted list. Example: [1: 01/30/2018 13:34:00 - Hello, Twitter!]
for i in range(len(date_list)):
    print('{}:  {} - {}'.format(i+1, date_list[i][0].strftime('%m/%d/%Y %H:%M:%S'),date_list[i][1][:80]))

# Make observations and display them, based on data.
days = str(tweet_date_end-tweet_date_begin).partition(',')[0].partition(' ')
print('Twitter User: @{} '.format(twitter_target))
print('Target date range was {} EST to {} EST.'.format(tweet_date_begin.strftime('%m/%d/%Y %H:%M:%S'), tweet_date_end.strftime('%m/%d/%Y %H:%M:%S')))
print('@{} posted a total of {} tweets within {} days.'.format(twitter_target, len(date_list), days[0]))
