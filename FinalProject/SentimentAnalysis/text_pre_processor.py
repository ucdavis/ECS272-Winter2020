# extract tweets using user id @tweet_extract.py
# second col of each row stores the tweet
# tokenizing, remove stop words
# remove hyperlink, handles, punctuation
# Lemmatization instead of stemming to preserve actual words
# csv: date, original tweet, [processed]
import csv
import os
import tweet_extract
import re
import nltk
import string
from nltk.tokenize import TweetTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tag import pos_tag

# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
en_stops = set(stopwords.words('english'))


def process():
    with open("output_got.csv", 'r') as fin, \
            open("new_output_got.csv", "w", newline='') as fout:
        reader = csv.reader(fin, delimiter=',')
        writer = csv.writer(fout)
        tweet_tokenizer = TweetTokenizer()
        # Lemmatization normalizes a word with the context of vocabulary and morphological analysis of words in text
        lemmatizer = WordNetLemmatizer()
        writer.writerow(['DateTime', 'Original Tweet', 'Processed Tweet'])
        for row in reader:
            useful = []
            lem = []
            text = row[1]
            # tokenizing
            tokens = tweet_tokenizer.tokenize(text)
            # stemming vs lemmatization, lemmatization is more accurate
            for word, tag in pos_tag(tokens):
                # ref: https://www.digitalocean.com/community/tutorials/how-to-perform-sentiment
                # -analysis-in-python-3-using-the-natural-language-toolkit-nltk
                word = re.sub("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", '',
                              word)
                word = re.sub("(@[A-Za-z0-9_]+)", "", word)
                word = re.sub("[\d]", "", word)
                if tag.startswith('NN'):
                    pos = 'n'
                elif tag.startswith('VB'):
                    pos = 'v'
                else:
                    pos = 'a'
                word = lemmatizer.lemmatize(word, pos)
                if len(word) > 0 and word not in string.punctuation:
                    lem.append(word.lower())
            # remove stop words
            for word in lem:
                if word not in en_stops:
                    useful.append(word)
            row.append(useful)
            writer.writerow(row)
        fin.close()
        fout.close()
    os.remove('output_got.csv')


if __name__ == "__main__":
    tweet_extract.extract_tweet_1()
    process()
