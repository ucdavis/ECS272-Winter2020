import GetOldTweets3 as got
import datetime
import csv

#id = 14874721
#username = pulvereyes

#start date: 2012.9.4
#end date: 2013.8.1


def extract_tweet_1():
    tweetCriteria = got.manager.TweetCriteria().setUsername("pulvereyes").setSince("2012-09-04").setUntil("2013-08-01")
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)
    user_tweets = [[tweet.date, tweet.text] for tweet in tweets]
    with open('output_got.csv', 'w+', newline='') as file:
        writer = csv.writer(file)
        for tweet in user_tweets:
            writer.writerow(tweet)
        file.close()


def extract_tweet_2():
    #username2 =realDonaldTrump
    tweetCriteria2 = got.manager.TweetCriteria().setUsername("realDonaldTrump").setSince("2012-09-04").setUntil("2012-10-01")
    tweets2 = got.manager.TweetManager.getTweets(tweetCriteria2)
    user_tweets2 = [[tweet.date, tweet.text] for tweet in tweets2]
    with open('output2_got.csv', 'w+', newline='') as file2:
        writer2 = csv.writer(file2)
        for tweet in user_tweets2:
            writer2.writerow(tweet)
        file2.close()


#if __name__ == "__main__":
    #extract_tweet_1()
    #extract_tweet_2()
