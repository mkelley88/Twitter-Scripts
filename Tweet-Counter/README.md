**Tweet-Counter.py**
-------------------
This script was written to count tweets from Twitter between two specific dates/times. It uses Tweepy for the API library. You must add in your own API keys/secrets from Twitter in order to use. As of v0.3 you will need to place these in a file called "twitter-keys.txt" in the same folder as the main script. 

**Bugs / Changelist**
------------------

**[v0.3 - Jan 29, 2018](Twitter-Scripts/Tweet_Counter.py)** (Current Version)
--------------------
- Major changes. Much of code was replaced.
- Now uses external file "twitter_keys.txt" to store Twitter secrets and keys.
- Accuracy improved!

**[0.1 - Jan 20, 2018](Twitter-Scripts/old_versions/Tweet-Counter.py)**
--------------------
- It should be noted, the printout showing the date and number of tweets for that day is inaccurate.
- Example:
  01-01-2018: 5 where 5 is the number of tweets in the previous 24 hour period. I will fix this soon. 
