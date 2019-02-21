from twython import Twython
import pandas as pd
import json
import datetime
import csv

# credentials
# tweeter credentials
with open('twitter_credentials.json', 'r') as file:
    content = file.read()
    credentials = json.loads(content)
    consumer_key = credentials['CONSUMER_KEY']
    consumer_secret = credentials['CONSUMER_SECRET']
    access_key = credentials['ACCESS_TOKEN']
    access_secret = credentials['ACCESS_SECRET']

APP_KEY = consumer_key
APP_SECRET = consumer_secret

twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
ACCESS_TOKEN = twitter.obtain_access_token()


twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)

hashtag_replies = []


def fetch_hashtag_tweets(hashtag):

    for i in range(101):
        try:
            temp = twitter.search(q='#' + hashtag + ' -filter:retweets',
                                  lang='en',
                                  result_type='recent',
                                  count=100,
                                  trim_user=False,
                                  include_entities=True,
                                  max_id=None if i == 0 else [x['id'] for x in hashtag_replies[-1]['statuses']][-1] - 1,
                                  tweet_mode='extended')
            hashtag_replies.append(temp)
        except Exception as e:
            print(e)
            break

    tweets_users_df = pd.DataFrame()
    for tweets in hashtag_replies:
        tweets_temp = pd.DataFrame(tweets['statuses'])
        tweets_temp.columns = ['tweet_' + t for t in tweets_temp.columns]
        users_temp = pd.DataFrame([x['user'] for x in tweets['statuses']])
        users_temp.columns = ['user_' + u for u in users_temp.columns]

        tweets_users_temp = pd.concat([tweets_temp, users_temp], axis=1)
        tweets_users_df = tweets_users_df.append(tweets_users_temp)

    all([tweet_id == user_id for tweet_id, user_id in
         zip([x['id'] for x in tweets_users_df['tweet_user']], tweets_users_df['user_id'])])

    current_date = datetime.datetime.today().strftime('%Y-%m-%d')
    tweets_users_df.to_csv(f'C:/Users/botieno/Desktop/ML_/twitter_data/{hashtag}_tweets_{current_date}.csv', index=False)


if __name__ == '__main__':
    fetch_hashtag_tweets(input('Enter the name of the hashtag you would like to extract'))


