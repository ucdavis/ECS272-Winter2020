# extract tweets using user id @tweet_extract.py
# second col of each row stores the tweet
# tokenizing, remove stop words
# lemmatization instead of stemming to preserve actual words
# [date, original tweet, stemming, lemmatization]
import csv
import os
import tweet_extract
#from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords


# nltk.download('stopwords')
# nltk.download('wordnet')
en_stops = set(stopwords.words('english'))


def process():
    with open("output_got.csv", 'r') as fin, \
            open("new_output_got.csv", "w", newline='') as fout:
        reader = csv.reader(fin, delimiter=',')
        writer = csv.writer(fout)
        #ps = PorterStemmer()
        lemmatizer = WordNetLemmatizer()
        for row in reader:
            useful = []
            #stemming = []
            lem = []
            text = row[1]
            # tokenizing
            words = text.split(" ")
            # remove stop words
            for word in words:
                if word not in en_stops:
                    useful.append(word)
            #row.append(useful)
            # stemming vs lemminization
            for word in useful:
                #stemming.append(ps.stem(word))
                lem.append(lemmatizer.lemmatize(word))
            #row.append(stemming)
            row.append(lem)
            writer.writerow(row)
        fin.close()
        fout.close()
    os.remove('output_got.csv')


if __name__ == "__main__":
    tweet_extract.extract_tweet_1()
    process()
