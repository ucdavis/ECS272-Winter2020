import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import json
from flask import Flask, request, render_template
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
app = Flask(__name__, template_folder="templates", static_folder="static", static_url_path="/static")

@app.route("/")
def output():
    return render_template("index.html")

@app.route("/loadData")
def output1():
    df = pd.read_csv('input/responses.csv')
    #df = df.head(10)
    df.dropna(inplace=True)
    df = processData(df, 3)
    #print(centroids)
    #print(type(X2[:,0]))
    #print(len(kmeans.labels_))
    return json.dumps(df.to_dict(orient = "records"))

@app.route("/cluster", methods=["POST"])
def changeCluster():
    #print(json.loads(request.data)["dat"][0])
    df = pd.DataFrame.from_records(json.loads(request.data)["dat"])
    #print(df.iloc[0])
    #df = pd.read_json(json.loads(request.data)["dat"])
    df.drop(columns=['X'], inplace=True, axis = 1)
    df.drop(columns=['Y'], inplace=True, axis = 1)
    df.drop(columns=['cluster'], inplace=True, axis = 1)
    df = processData(df, int(json.loads(request.data)["clusterNum"], base=10))
    return json.dumps(df.to_dict(orient = "records"))


def processData(df, clusterNum):
    X = np.array(df.iloc[:,:19])
    #df.drop(df.columns.difference(['Music','Slow songs or fast songs', 'Dance, Disco, Funk', 'Folk music', 'Country', 'Classical', 'Musicals', 'Pop', 'Rock', 'Metal, Hard rock', 'Punk', 'Hip hop, Rap', 'Reggae, Ska', 'Swing, Jazz', 'Rock n Roll', 'Alternative music', 'Latin', 'Techno, Trance', 'Opera']), 1, inplace=True)
    #print(df.iloc[0])
    #print(df.to_dict(orient = "records")[1])
    kmeans = KMeans(n_clusters=clusterNum).fit(X)  #parameters to change
    pca = PCA(n_components=2) #TODO remove PCA data to diff function 
    pca.fit(X)
    X_trans = pca.transform(X) # 2d dimension reduction for x,y axis
    X1 = X_trans[:,0].tolist()
    X2 = X_trans[:,1].tolist()
    labels = kmeans.labels_.tolist()
    df['X'] = X1
    df['Y'] = X2
    df['cluster'] = labels
    return df

if __name__ == "__main__":
	app.run()
