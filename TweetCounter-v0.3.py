#!/usr/bin/python3
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
        try:
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token_key, access_token_secret)
            api = tweepy.API(auth)
        except:
            print('INTERNET CONNECTION ERROR!')

except IOError as err:
    print('\n---ERROR!---\n{0}\nMake sure to place this file in the same folder as this script!\n'.format(err))
    raise SystemExit(0)
except gaierror:
    print('giaerror!!!')
    raise SystemExit(0)

### Optional Function (Unused) ### 
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
                date_list.append([created_at_est, tweet.text[:80]])
            elif date_begin < created_at_est:
                pass
            else:
                break
        return date_list

##### MAIN PROGRAM BEGINS HERE #####
# Get list of tweet dates and store them in a list. eg [DATE, "Tweet text"]
date_list = get_tweets(api, twitter_target, tweet_date_begin, tweet_date_end)

# Display formatted list.
for i in range(len(date_list)):
    print('{}:  {} - {}'.format(i+1, date_list[i][0].strftime('%m/%d/%Y %H:%M:%S'),date_list[i][1][:80]))

avg = []
ht, mt, st = 0, 0, 0

for i in range(len(date_list)-1):
    avg.append([date_list[i][0].hour, date_list[i][0].minute, date_list[i+1][0].second])
    h = avg[i][0]; m = avg[i][1]; s = avg[i][2]; 
    for h in range(24):
        ht+=h
        for m in range(60):
            mt+=m
            for s in range(60):
                st+=s
h=round(h/len(avg),2); m=round(m/len(avg),2); s=round(s/len(avg),2);

print('Hours: {} Minutes: {} Seconds: {}'.format(h,m,s))
#print(avg)
#avg = avg/i
#print(avg)

# Make observations and display them, based on data.
days = str(tweet_date_end-tweet_date_begin).partition(',')[0].partition(' ')
print('Twitter User: @{} '.format(twitter_target))
print('Target date range was {} EST to {} EST.'.format(tweet_date_begin.strftime('%m/%d/%Y %H:%M:%S'), tweet_date_end.strftime('%m/%d/%Y %H:%M:%S')))
print('@{} posted a total of {} tweets within {} days.'.format(twitter_target, len(date_list), days[0]))

