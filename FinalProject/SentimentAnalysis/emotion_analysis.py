# Basic Emotion Analysis to derive the basic emotions revealed by individual tweets at specific time points.
import csv
import nltk
from nltk.corpus import wordnet


# nltk.download('wordnet')
emotion_categories = ['anger', 'fear', 'anticipation', 'surprise', 'joy', 'sadness', 'trust', 'disgust']
# Read NRC-VAD to get VAD scores for each word
dic_VAD = dict()
dic_VAD['aaaaaaah'] = []
index = 0
for line_vad in open("NRC-VAD-Lexicon.txt", "r"):
    index += 1
    if index < 2:
        continue
    line_vad = line_vad.strip()
    listFromLine_vad = line_vad.split('\t')
    if listFromLine_vad[0] not in dic_VAD.keys():
        dic_VAD[listFromLine_vad[0]] = []
    dic_VAD[listFromLine_vad[0]].append(listFromLine_vad[1])
    dic_VAD[listFromLine_vad[0]].append(listFromLine_vad[2])
    dic_VAD[listFromLine_vad[0]].append(listFromLine_vad[3])
# print dic_VAD

# Read NRC-Emotion to get emotion categories for each word
dic_category = dict()
dic_category['abacus'] = []
for line in open("NRC-Emotion-Lexicon-Wordlevel-v0.92.txt", "r"):
    line = line.strip()
    listFromLine = line.split('\t')
    if listFromLine[2] == '1' and listFromLine[1] != 'positive' and listFromLine[1] != 'negative':
        if listFromLine[0] not in dic_category.keys():
            dic_category[listFromLine[0]] = []
        dic_category[listFromLine[0]].append(listFromLine[1])
# print dic_category['abhor']


def get_category_score():
    with open("new_output_got.csv", 'r') as fin:
        reader = csv.reader(fin, delimiter=',')
        for row in reader:
            result_list = [0 for _ in range(32)]
            '''
            dic = dict(c1=0, V1=0, A1=0, D1=0, c2=0, V2=0, A2=0, D2=0, c3=0, V3=0, A3=0, D3=0,
                       c4=0, V4=0, A4=0, D4=0, c5=0, V5=0, A5=0, D5=0, c6=0, V6=0, A6=0, D6=0,
                       c7=0, V7=0, A7=0, D7=0, c8=0, V8=0, A8=0, D8=0)
                       '''
            words = row[2].split(" ")
            words[0] = words[0][1:len(words[0])]
            for word in words:
                word = word[1:len(word) - 2]
                # print word
                # if word[0] == '#' or (len(word) > 7 and word[0:7] == 'http://'):
                #    continue
                if not word.isalpha():
                    continue
                word = word.lower()
                # Get the emotion categories of the word through NRC-Emotion Category database
                if word in dic_category.keys() and dic_VAD.keys():
                    for category in dic_category[word]:
                        position = emotion_categories.index(category)
                        result_list[4 * position] += 1
                        # Get the VAD scores of the word through NRC-VAD database
                        result_list[4 * position + 1] += float(dic_VAD[word][0])
                        result_list[4 * position + 2] += float(dic_VAD[word][1])
                        result_list[4 * position + 3] += float(dic_VAD[word][2])
                else:
                    # Find all the synonyms of this word in the WordNet database
                    synonyms = []
                    syns = wordnet.synsets(word)
                    for syn in syns:
                        for synonym in syn.lemma_names():
                            if synonym in synonyms:
                                continue
                            synonyms.append(synonym)
                    # Find the emotion categories of all the synonyms through NRC-Emotion Category database
                    synonyms_result_list = [0 for _ in range(32)]
                    for synonym in synonyms:
                        if synonym in dic_category.keys() and synonym in dic_VAD.keys():
                            for synonym_category in dic_category[synonym]:
                                synonym_position = emotion_categories.index(synonym_category)
                                # result_list[4 * position] += 1
                                synonyms_result_list[4 * synonym_position] += 1
                                # Get the VAD scores of all the synonyms through NRC-VAD database
                                synonyms_result_list[4 * synonym_position + 1] += float(dic_VAD[synonym][0])
                                synonyms_result_list[4 * synonym_position + 2] += float(dic_VAD[synonym][1])
                                synonyms_result_list[4 * synonym_position + 3] += float(dic_VAD[synonym][2])
                    for i in range(0, 8):
                        if synonyms_result_list[4 * i] > 0:
                            result_list[4 * i] += 1
                            valence_average = synonyms_result_list[4 * i + 1] / synonyms_result_list[4 * i]
                            result_list[4 * i + 1] += valence_average
                            arousal_average = synonyms_result_list[4 * i + 2] / synonyms_result_list[4 * i]
                            result_list[4 * i + 2] += arousal_average
                            dominance_average = synonyms_result_list[4 * i + 3] / synonyms_result_list[4 * i]
                            result_list[4 * i + 3] += dominance_average
            # Get the final result vector for this tweet
            category_sum = 0
            valence_sum = 0
            arousal_sum = 0
            dominance_sum = 0
            for j in range(0, 8):
                category_sum += result_list[4 * j]
                valence_sum += result_list[4 * j + 1]
                arousal_sum += result_list[4 * j + 2]
                dominance_sum += result_list[4 * j + 3]
            for j in range(0, 8):
                if result_list[4 * j] > 0:
                    result_list[4 * j] = float(result_list[4 * j]) / float(category_sum)
                    result_list[4 * j + 1] = valence_sum / category_sum
                    result_list[4 * j + 2] = arousal_sum / category_sum
                    result_list[4 * j + 3] = dominance_sum / category_sum
            print result_list


if __name__ == "__main__":
    get_category_score()

