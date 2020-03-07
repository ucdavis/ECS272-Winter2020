import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy import loadtxt
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense
from keras import optimizers
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder
from keras.utils import to_categorical
from sklearn.preprocessing import StandardScaler


training_file = "./pokemon_alopez247.csv"
type_map = {'Normal':1, 'Grass':2, 'Ice':3, 'Flying':4, 'Ground':5, 'Dragon':6, 'Fairy':7, 'Electric':8, 'Bug':9, 'Psychic':10, 'Water':11, 'Rock':12, 'Dark':13, 'Ghost':14, 'Fire':15, 'Steel':16, 'Fighting':17, 'Poison':18}
legendary_map = {False:0,   True:1}

df = pd.read_csv(training_file)
x = df.iloc[:, 4].values.reshape(-1,1)
# x = df.iloc[:, 4:11].values
sc = StandardScaler()
x = sc.fit_transform(x)
y = df.iloc[:, 12]
y = y.replace(legendary_map).values.reshape(-1,1)
# y = y.replace(type_map).values.reshape(-1,1)
y = to_categorical(y)

model = Sequential()
model.add(Dense(20, input_dim=1, kernel_initializer='normal', activation='relu'))
model.add(Dense(15, activation='relu'))
model.add(Dense(2, activation='softmax'))
# model.add(Dense(19, activation='softmax'))
model.summary()
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

history = model.fit(x, y, epochs=100, batch_size=10,  verbose=1)

_, accuracy = model.evaluate(x, y)
print('Accuracy: %.2f' % (accuracy*100))

model.save("pokemon_model.h5")
print("Saved model to the disk")
