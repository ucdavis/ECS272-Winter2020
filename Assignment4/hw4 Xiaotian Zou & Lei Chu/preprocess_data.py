import gensim.downloader as api
import numpy as np
word_vectors = api.load("glove-wiki-gigaword-100")

def find_vector(inputs):
    result = []
    # inputs = inputs.split()
    for word in inputs:
        try:
            if word == ' ':
                continue
            if  result == []:
                result.append(np.array(word_vectors[word]))
            else:
                result[-1] += np.array(word_vectors[word])
        except KeyError:
            pass
        continue
    
    return np.array(result)



# import csv
# import json

# def read_file():
#     genre, keywords, date, popularity, vote = [], [], [], [], []
#     with open('tmdb_5000_movies.csv', 'r') as f:
#         movie_data = csv.reader(f)
#         for line in movie_data:
#             genre.append(line[1])
#             keywords.append(line[4])
#             date.append(line[11])
#             popularity.append(line[8])
#             vote.append(line[18])
#     return genre[1:], keywords[1:], date[1:], popularity[1:], vote[1:]

# def convert_string_to_json(str):
#     return json.loads(str)

# def get_json_array_content(str):
#     result = []
#     json_data = convert_string_to_json(str)
#     for line in json_data:
#         result.append(line['name'])
#     return result

# def get_content_list(data):
#     result = []
#     for line in data:
#         result.append(get_json_array_content(line))
#     return result

# def get_one_hot(genre_list):
#     result = []
#     for line in genre_list:
#         one_hot = [0] * 20
#         for entry in line:
#             if entry == 'Action':
#                 one_hot[0] = 1
#             elif entry == 'Adventure':
#                 one_hot[1] = 1
#             elif entry == 'Fantasy':
#                 one_hot[2] = 1
#             elif entry == 'Science Fiction':
#                 one_hot[3] = 1
#             elif entry == 'Crime':
#                 one_hot[4] = 1
#             elif entry == 'Drama':
#                 one_hot[5] = 1
#             elif entry == 'Thriller':
#                 one_hot[6] = 1
#             elif entry == 'Animation':
#                 one_hot[7] = 1
#             elif entry == 'Family':
#                 one_hot[8] = 1
#             elif entry == 'Western':
#                 one_hot[9] = 1
#             elif entry == 'Comedy':
#                 one_hot[10] = 1
#             elif entry == 'Romance':
#                 one_hot[11] = 1
#             elif entry == 'Horror':
#                 one_hot[12] = 1
#             elif entry == 'Mystery':
#                 one_hot[13] = 1
#             elif entry == 'History':
#                 one_hot[14] = 1
#             elif entry == 'War':
#                 one_hot[15] = 1
#             elif entry == 'Music':
#                 one_hot[16] = 1
#             elif entry == 'Documentary':
#                 one_hot[17] = 1
#             elif entry == 'Foreign':
#                 one_hot[18] = 1
#             elif entry == 'TV Movie':
#                 one_hot[19] = 1
#         result.append(one_hot)
#     print(result)
#     return result

# def count_genre(target_arr, genre, target_index):
#     if genre[target_index] == 1:
#         target_arr.append(1)
#     else:
#         target_arr.append(0)
#     return target_arr



# def get_year_genre_count(date, genre_onehot):
#     year_list = []
#     action_count, adventure_count, fantacy_count, science_fiction_count, \
#         crime_count, drama_count, thriller_count, animation_count, family_count, \
#             western_count, comedy_count, romance_count, horror_count, mystery_count, \
#                 history_count, war_count, music_count, documentary_count, \
#                     foreign_count, tv_movie_count = [], [], [], [], [], [], [], [], []\
#                         , [], [], [], [], [], [], [], [], [], [], []
    
#     for i in range(len(date)):
#         tmp_year = date[i][0:4]
#         if tmp_year not in year_list:
#             year_list.append(tmp_year)
#             action_count = count_genre(action_count, genre_onehot, 0)
#             adventure_count = count_genre(adventure_count, genre_onehot, 1)
#             fantacy_count = count_genre(fantacy_count, genre_onehot, 2)
#             science_fiction_count = count_genre(science_fiction_count, genre_onehot, 3)
#             crime_count = count_genre(crime_count, genre_onehot, 4)
#             drama_count = count_genre(drama_count, genre_onehot, 5)
#             thriller_count = count_genre(thriller_count, genre_onehot, 6)
#             animation_count = count_genre(animation_count, genre_onehot, 7)
#             family_count = count_genre(family_count, genre_onehot, 8)
#             western_count = count_genre(western_count, genre_onehot, 9)
#             comedy_count = count_genre(comedy_count, genre_onehot, 10)
#             romance_count = count_genre(romance_count, genre_onehot, 11)
#             horror_count = count_genre(horror_count, genre_onehot, 12)
#             mystery_count = count_genre(mystery_count, genre_onehot, 13)
#             history_count = count_genre(history_count, genre_onehot, 14)
#             war_count = count_genre(war_count, genre_onehot, 15)
#             music_count = count_genre(music_count, genre_onehot, 16)
#             documentary_count = count_genre(documentary_count, genre_onehot, 17)
#             foreign_count = count_genre(foreign_count, genre_onehot, 18)
#             tv_movie_count = count_genre(tv_movie_count, genre_onehot, 19)
#         else:
#             if genre_onehot[0] == '1':
#                 action_count[-1] += 1
#             if genre_onehot[1] == '1':
#                 adventure_count[-1] += 1
#             if genre_onehot[2] == '1':
#                 fantacy_count[-1] += 1
#             if genre_onehot[3] == '1':
#                 science_fiction_count[-1] += 1
#             if genre_onehot[4] == '1':
#                 crime_count[-1] += 1
#             if genre_onehot[5] == '1':
#                 drama_count[-1] += 1
#             if genre_onehot[6] == '1':
#                 thriller_count[-1] += 1
#             if genre_onehot[7] == '1':
#                 animation_count[-1] += 1
#             if genre_onehot[8] == '1':
#                 family_count[-1] += 1
#             if genre_onehot[9] == '1':
#                 western_count[-1] += 1
#             if genre_onehot[10] == '1':
#                 comedy_count[-1] += 1
#             if genre_onehot[11] == '1':
#                 romance_count[-1] += 1
#             if genre_onehot[12] == '1':
#                 horror_count[-1] += 1
#             if genre_onehot[13] == '1':
#                 mystery_count[-1] += 1
#             if genre_onehot[14] == '1':
#                 history_count[-1] += 1
#             if genre_onehot[15] == '1':
#                 war_count[-1] += 1
#             if genre_onehot[16] == '1':
#                 music_count[-1] += 1
#             if genre_onehot[17] == '1':
#                 documentary_count[-1] += 1
#             if genre_onehot[18] == '1':
#                 foreign_count[-1] += 1
#             if genre_onehot[19] == '1':
#                 tv_movie_count[-1] += 1

#     return year_list, action_count, adventure_count, fantacy_count, science_fiction_count, \
#         crime_count, drama_count, thriller_count, animation_count, family_count, \
#             western_count, comedy_count, romance_count, horror_count, mystery_count, \
#                 history_count, war_count, music_count, documentary_count, \
#                     foreign_count, tv_movie_count        
    

# if __name__ == "__main__":
#     genre_original,keywords_original, \
#         date_list, popularity_list, vote_list = read_file()

#     genre_list = get_content_list(genre_original)
#     keywords_list = get_content_list(keywords_original)
#     genre_onehot = get_one_hot(genre_list)

#     genre_onehot = get_year_genre_count(date_list, genre_onehot)


#     year_list, action_count, adventure_count, fantacy_count, science_fiction_count, \
#         crime_count, drama_count, thriller_count, animation_count, family_count, \
#             western_count, comedy_count, romance_count, horror_count, mystery_count, \
#                 history_count, war_count, music_count, documentary_count, \
#                     foreign_count, tv_movie_count = get_year_genre_count(date_list, genre_onehot)
    
#     print('hi')