# ECS 272 HW4
#
# Written by Jingwei Wan and Mingye Fu


import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.decomposition import FactorAnalysis
from sklearn.neighbors import LocalOutlierFactor


def OriginalData():
    return pd.read_csv('student-mat.csv')

def encode(data): # encode non-number entries
    le = preprocessing.LabelEncoder()
    data_encoded = data.copy()
    for i in data.columns:
        if data[i].dtypes == 'object':
            data_encoded[i] = le.fit_transform(data[i])

    return data_encoded

def make_header(n_feature):
    header = []
    for i in range(n_feature):
        txt = "feature"+ str(i+1)
        header.append(txt)
    return header

def remove_outlier(data):
    # Local Outlier Factor to identify outliers
    clf = LocalOutlierFactor(n_neighbors=100, contamination='auto')
    data_revised = encode(data)
    pred = clf.fit_predict(data_revised)

    # remove outliers decided from Local Outlier Factor
    drop_list = []
    for i in range(len(pred)):
        if pred[i] != 1:
            drop_list.append(i)
    data_revised = data.drop(drop_list)
    return data_revised


def factor_analysis(X, y, n_feature): # factor analysis to n_features
    transformer = FactorAnalysis(n_components=n_feature, random_state=0)
    data_transformed = transformer.fit_transform(X, y)
    X_reduced = pd.DataFrame(data_transformed)
    X_reduced.columns = make_header(n_feature)
    return X_reduced

# ============= select features with high correlation ===================
def select_first_n(data, X_header, y_header, n):
    feature_list = []
    X = data.loc[:, X_header]
    y = data.loc[:, y_header]

    # label all class in y
    le = preprocessing.LabelEncoder()

    # label all class in X
    for i in X_header:
        if X[i].dtypes == 'object':
            X[i] = le.fit_transform(X[i])
        feature_list.append([i, abs(np.corrcoef(X[i], y)[0, 1])])

    feature_list = np.array(sorted(feature_list, key = lambda a:a[1], reverse = True))
    feature_list = feature_list[0:n,0].tolist()
    print('first', n, 'most correlated features:\n', feature_list)
    return data[feature_list]


if __name__ == '__main__':
    data = OriginalData()
    print(data.shape)
    data_revised = remove_outlier(data)
    print(data_revised.shape)

    header = data.columns
    n_max = 8
    n_feature = 3
    X_header = header[0:26].append(header[28:len(header)])
    y_header = header[26:28]

    X_selected = select_first_n(data_revised,X_header,y_header[0], n_max)
    print(X_selected.shape)

    y = data_revised.loc[:, y_header]

    X_encoded = encode(X_selected)
    X_reduced = factor_analysis(X_encoded, y[y_header[0]], n_feature)
    print(X_reduced)





