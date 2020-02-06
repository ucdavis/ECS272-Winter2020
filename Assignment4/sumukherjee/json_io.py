import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import json
from flask import Flask, request, render_template
from sklearn.cluster import KMeans
app = Flask(__name__, template_folder="templates", static_folder="static", static_url_path="/static")

@app.route("/output")
def output():
    
    return render_template("index.html")

@app.route("/output1")
def output1():
    df = pd.read_csv('responses.csv')
    #df = df.head(10)
    df.dropna(inplace=True)
    df.drop(df.columns.difference(['Music','Slow songs or fast songs', 'Dance, Disco, Funk', 'Folk music', 'Country', 'Classical', 'Musicals', 'Pop', 'Rock', 'Metal, Hard rock', 'Punk', 'Hip hop, Rap', 'Reggae, Ska', 'Swing, Jazz', 'Rock n Roll', 'Alternative music', 'Latin', 'Techno, Trance', 'Opera']), 1, inplace=True)
    print(df.iloc[0])
    #print(df.to_dict(orient = "records")[1])
    kmeans = KMeans(n_clusters=3).fit(df)
    centroids = kmeans.cluster_centers_
    print(centroids)
    print(len(kmeans.labels_))
    print(kmeans.cluster_centers_)
    return json.dumps(df.to_dict(orient = "records"))

if __name__ == "__main__":
	app.run()