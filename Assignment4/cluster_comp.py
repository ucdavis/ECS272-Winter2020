#helper file 

import pandas as pd

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

import plotly.express as px
import plotly.graph_objects as go

import pickle
import numpy as np
from numpy import nan

#globals
MAX_CLUSTERS = 7

#category conversions, arranged in "ascending" order
cat_ordered_values = {
    'Smoking':['never smoked','tried smoking','former smoker','current smoker'],
    'Alcohol':['never','social drinker','drink a lot'],
    'Punctuality':['i am often early','i am always on time','i am often running late'],
    'Lying':['never','only to avoid hurting someone','sometimes','everytime it suits me'],
    'Internet usage':['no time at all','less than an hour a day','few hours a day','most of the day'],
    'Gender':['female','male'],
    'Left - right handed':['right handed','left handed'],
    'Education':['currently a primary school pupil','primary school','secondary school','college/bachelor degree','masters degree','doctorate degree'],
    'Only child':['no','yes'],
    'Village - town':['village','city'],
    'House - block of flats':['block of flats','house/bungalow'],
}

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


#convert a pandas categorical column to its corresponding numbers
def column_cat_to_num(df_col):
    
    new_col = pd.Series(dtype = np.float64,name = df_col.name)
    
    #get range of unique values
    these_order = cat_ordered_values[df_col.name]
    
    #scaling for 0-4 (add 1 later)
    scaling = 4/(len(these_order) - 1)
    
    #calculate new list of values
    new_vals = []
    for cat_val in df_col:
        if cat_val is nan:
            new_vals.append(nan)
            continue
        else:
            new_vals.append(scaling * these_order.index(cat_val) + 1)
            
            
    #make the new column
    new_col = pd.Series(data = new_vals, dtype = np.float64, name = df_col.name)
    
    return new_col
    

#convert categorical data to range 1-5
def categorical_convert(data):
    
    #get just the categorical data
    cat_data = data.select_dtypes(['object'])
    
    #convert the categorical data
    for col in cat_data:
        data[col] = column_cat_to_num(cat_data[col])
    
    
    return data

#read in data
try:
    with open("__temp", 'rb') as f:
        df = pickle.load(f)
except:
    # load responses as a DataFrame
    with open("responses.csv") as f:
        df = pd.read_csv(f)
    #convert categories to integers, within range 1-5
    df = categorical_convert(df)
    df.fillna(df.mean(), inplace=True)
    df = all_clusters(df)
    # write file, so is easy to load next time
    with open("__temp", "wb") as f:
        pickle.dump(df, f)


