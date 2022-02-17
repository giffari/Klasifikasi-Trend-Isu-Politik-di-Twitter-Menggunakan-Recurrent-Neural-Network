import os, csv, random
import tweepy as tw

os.system("clear")

consumer_key= "3Ys8PPUlCcxqx9uon3cgofeQJ"
consumer_secret= "iBfV9X2nv2PIF77CwH4YE7cISa1LT74iVgpKBDFM1X6daePk9E"
access_token= "892330049675735042-PdnuZ2N0gdCvyGa5cHlGMG5EPQqBM7D"
access_token_secret= "niKYLtUA2UQFxoPuuCVUQ5lfNekOqtYDJe31nwd2iNXVF"

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

# Define the search term and the date_since date as variables
search_words = "politik"
date_since = "2020-07-01"
new_search = search_words + " -filter:retweets"

# Collect tweets
tweets = tw.Cursor(api.search,
                    tweet_mode="extended",
                    q=new_search,
                    lang="id",
                    since=date_since).items(10)

with open('tweets_10000_labeled_10.csv', 'w', newline='') as target:
        writer = csv.writer(target)
        writer.writerow(['label', 'created_at', 'tweet_id', 'tweet_text', 'retweet_count', 'favorite_count', 'tweet_lang', 'user_id', 'user_name', 'user_screen_name', 'user_since', 'user_time_zone', 'user_verified'])
        for tweet in tweets:
            varJson = tweet._json; varUser = varJson['user']
            label = random.choice(['negatif','positif','netral'])
            writer.writerow([label, varJson['created_at'], varJson['id'], varJson['full_text'], varJson['retweet_count'], varJson['favorite_count'], varJson['lang'], varUser['id'], varUser['name'], varUser['screen_name'], varUser['created_at'], varUser['time_zone'], varUser['verified']])
            print('{} : {}'.format(varUser['id'],varJson['full_text']))
