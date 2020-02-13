class Cluster(object):
    import pandas as pd
    from sklearn.cluster import KMeans
    import numpy as np

    def __init__(self, filename):
        self.df = self.pd.read_csv(filename)
        self.head = list(self.df.columns)

    def getCluster(self, k, index1, index2):
        twoD = self.df.to_numpy()
        a1 = twoD[:, index1:index1+1]
        a2 = twoD[:, index2:index2+1]
        twoD_array = self.np.concatenate((a1, a2), axis = 1)
        kmeans = self.KMeans(n_clusters = k).fit_predict(X = twoD_array)
        data = []
        for i in range(len(kmeans)):
            data.append((kmeans[i], twoD_array[i][0], twoD_array[i][1]))
        clustering_df = self.pd.DataFrame(data, columns=['K-Means', self.head[index1], self.head[index2]])
        return clustering_df

c = Cluster('pokemon_alopez247.csv')
c.getCluster(3, 6, 19)