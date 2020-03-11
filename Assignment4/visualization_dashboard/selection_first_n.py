import pandas as pd
from sklearn import preprocessing
import numpy as np


# ============= remove features with low correlation ===================
def selection_first_n(data, X_header, y_header, n):
    feature_list = []
    X = data.loc[:, X_header]
    y = data.loc[:, y_header]

    # label all class in y
    le = preprocessing.LabelEncoder()
    y = le.fit_transform(y)

    # label all class in X
    for count, i in enumerate(X_header):
        if X[i].dtypes == 'object':
            le = preprocessing.LabelEncoder()
            X[i] = le.fit_transform(X[i])
        feature_list.append([i, np.abs(np.corrcoef(X[i], y)[0, 1])])

    feature_list = np.array(sorted(feature_list, key = lambda a:a[1], reverse = True))
    return feature_list[0:n, 0]

if __name__ == '__main__':
    data = pd.read_csv('student-mat.csv')
    header = data.columns
    n = 8
    X_header = header[0:26].append(header[29:len(header)])
    y_header = header[26]
    feature_list = selection_first_n(data, X_header, y_header, n)
    print('first', n, 'most correlated features:\n', feature_list)
