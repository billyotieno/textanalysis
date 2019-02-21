# -*- coding: utf-8 -*-

import tweepy
import csv
import json

# tweeter credentials
with open('twitter_credentials.json', 'r') as file:
    content = file.read()
    credentials = json.loads(content)
    consumer_key = credentials['CONSUMER_KEY']
    consumer_secret = credentials['CONSUMER_SECRET']
    access_key = credentials['ACCESS_TOKEN']
    access_secret = credentials['ACCESS_SECRET']

print(credentials)


# authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


def get_all_user_tweets(screen_name):
    """ get_all_user_tweets is used to fetch tweets from a particular tweeter user

        Args: screen_name - Username of the tweeter account
        Returns: 0 - the function doesn't return an output but generates a csv with all the tweets
    """

    # list to hold all the tweets
    tweets_list = []

    # fetching tweets with multiple requests of 200 each
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)
    tweets_list.extend(new_tweets)
    old_tweet = tweets_list[-1].id - 1

    # extracting all tweets
    while len(new_tweets) > 0:
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=old_tweet)
        tweets_list.extend(new_tweets)
        old_tweet = tweets_list[-1].id - 1
        print(f"{len(tweets_list)} tweets, have been extracted so far")

    # tweet output
    tweetput = [[tweet.id_str, tweet.created_at, tweet.text.encode('utf-8')] for tweet in tweets_list]

    # file output: .csv
    with open(screen_name + "_tweets.csv", 'w', encoding='utf-8') as usertweets:
        writer = csv.writer(usertweets)
        writer.writerow(['id', 'created_at', 'text'])
        writer.writerows(tweetput)


def get_all_hashtag_tweets(hashtag, maximum_tweets):
    """ Function: get_all_hashtag_tweets()
            is used to fetch all the tweets of a particular hashtag e.g. #wilkinsfadhili etc.
        Args:
            hashtag - Hashtag definition (String only) - no special characters
            maximum_tweets - Maximum number of tweets to search
        Returns:
            Output is a text file with the extracted tweets

        q_string: to filter by data use since:2015-12-21 until:until:2015-12-21
    """

    for tweet in tweepy.Cursor(api.search, q='#'+hashtag, rpp=100).items(maximum_tweets):
        with open('tweets_with_hashtag' + hashtag + '.txt', 'w') \
                as hashtagtweets:
            hashtagtweets.write(str(tweet.text.encode('utf-8') + "\n".encode('ascii')))

    print(f"Extracted {maximum_tweets} for hashtag #{hashtag}")


if __name__ == '__main__':
    # objective
    objective = int(input("Select objective: \n 1. Fetch Hashtag Tweets \n 2. Fetch User Tweets"))
    if objective == 1:
        tag = str(input("Enter the hashtag to extract tweets from: "))
        max_number_tweets = int(input("Maximum number of tweets from the hashtag: "))
        get_all_hashtag_tweets(tag, max_number_tweets)
    elif objective == 2:
        get_all_user_tweets(input("Enter the tweeter handle of the person from which to extract the tweets: "))
    else:
        print("Sorry, the selected option is not in list")


