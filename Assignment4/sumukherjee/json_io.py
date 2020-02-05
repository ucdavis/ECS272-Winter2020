import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
from flask import Flask, request, render_template
app = Flask(__name__, template_folder="templates", static_folder="static", static_url_path="")

@app.route("/output")
def output():
    
    return render_template("index.html")

@app.route("/output1")
def output1():
    df = pd.read_csv('responses.csv')
    return df.to_json()

if __name__ == "__main__":
	app.run()