#helper file 

import pandas as pd

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

import plotly.express as px
import plotly.graph_objects as go

import pickle


#globals
MAX_CLUSTERS = 7


#calculate all clusters on start
def all_clusters(data):
    
    #remove non numerical data, to make clustering easier
    data_num = data.select_dtypes(['number'])
    
    #drop age, height, weight, num siblings, because they are not constrained to 1-5
    out_numlabels = ['Age','Height','Weight','Number of siblings']
    data_num = data_num.drop(axis = 1, labels = out_numlabels)
    
    #loop to do clustering
    for numCluster in range(2,MAX_CLUSTERS + 1):
        
        #get clusters
        kmeans = KMeans(n_clusters = numCluster)
        kmeans.fit(data_num)
        
        #add column of cluster grouping to data
        data['clusterGrouping' + str(numCluster)] = kmeans.labels_.astype(str)
    
    #do pca, to reduce to 3 axes
    reduce_dim_data_df = pd.DataFrame(PCA(n_components=3).fit_transform(data_num))
    
    #rename columns
    dims = ['x','y','z']
    for i in range(3):
        reduce_dim_data_df.rename(columns = {i: dims[i]+'coord'},inplace = True)
        
    #concatentate PCA values with data
    data = pd.concat([data,reduce_dim_data_df],axis = 1, sort = False)
    
    return data

#read in data
try:
    with open("__temp", 'rb') as f:
        df = pickle.load(f)
except:
    # load responses as a DataFrame
    with open("responses.csv") as f:
        df = pd.read_csv(f)
    df.fillna(df.mean(), inplace=True)
    df = all_clusters(df)
    # write file, so is easy to load next time
    with open("__temp", "wb") as f:
        pickle.dump(df, f)


