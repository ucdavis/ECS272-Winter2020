import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import json
from flask import Flask, request, render_template

app = Flask(__name__, template_folder="templates",
            static_folder="static", static_url_path="/static")


@app.route("/")
def output():
    return render_template("index.html")


@app.route("/loadData")
def output1():
    df = pd.read_json('input/artifacts.json')
    return json.dumps(processData(df))


def processData(df):
    df.drop(['_etag'], axis=1, inplace=True)
    df.drop(['repo_mined_version'], axis=1, inplace=True)
    df.drop(['repo_watchers'], axis=1, inplace=True)
    df.drop(['repo_members'], axis=1, inplace=True)
    df.drop(['merged_at'], axis=1, inplace=True)
    df.drop(['base_branch'], axis=1, inplace=True)
    df.drop(['branch'], axis=1, inplace=True)
    df.drop(['diff_url'], axis=1, inplace=True)
    df.drop(['_created'], axis=1, inplace=True)
    df.drop(['filtered_reason'], axis=1, inplace=True)
    df.drop(['image_tag'], axis=1, inplace=True)
    df.drop(['match'], axis=1, inplace=True)
    df.drop(['_links'], axis=1, inplace=True)
    df.drop(['_id'], axis=1, inplace=True)
    jsonDf = pd.io.json.json_normalize(df.classification)
    df = df.assign(test=jsonDf['test'], build=jsonDf['build'],
                   code=jsonDf['code'], exceptions=jsonDf['exceptions'], )
    jsonDf = pd.io.json.json_normalize(df.metrics)
    df = df.assign(
        changes=jsonDf['changes'], deletions=jsonDf['deletions'], additions=jsonDf['additions'])
    df.drop(['classification'], axis=1, inplace=True)
    df.drop(['metrics'], axis=1, inplace=True)
    jsonDf = pd.io.json.json_normalize(df.current_status)
    df = df.assign(
        status_time_stamp=jsonDf['time_stamp'], status=jsonDf['status'])
    df.drop(['current_status'], axis=1, inplace=True)
    df['reproduced'] = df['reproduced'].astype('bool')
    jsonDf = pd.io.json.json_normalize(df.failed_job)
    df = df.assign(os=jsonDf['config.os'])
    df['repo_commits'].replace(r'^\s*$', np.nan, regex=True, inplace=True)
    df['repo_commits'].fillna(0, inplace=True)
    df['repo_commits'] = df['repo_commits'].astype('int')
    df['repo_commits'].fillna(0, inplace=True)
    # dat = []
    # for index, row in df.iterrows():
    #     found = False
    #     for d in dat:
    #         if d['name'] == row['lang']:
    #             found = True
    #             foundChild = False
    #             for c in d['children']:
    #                 if c['name'] == row['build_system']:
    #                     foundChild = True
    #                     c['value'] = c['value'] + 1
    #             if not foundChild:
    #                 newChild = {}
    #                 newChild['name'] = row['build_system']
    #                 newChild['value'] = 1
    #                 d['children'].append(newChild)
    #     if not found:
    #         newD = {}
    #         newD['name'] = row['lang']
    #         newD['children'] = []
    #         newChild = {}
    #         newChild['name'] = row['build_system']
    #         newChild['value'] = 1
    #         newD['children'].append(newChild)
    #         dat.append(newD)
    for i, row in df.iterrows():
        patch = ''
        if row['build'] == 'Yes' or row['build'] == 'No':
            patch = 'Build'
        if row['test'] == 'Yes' or row['test'] == 'No':
            if len(patch) > 0:
                patch = patch + '+'
            patch = patch + 'Test'
        if row['code'] == 'Yes' or row['code'] == 'No':
            if len(patch) > 0:
                patch = patch + '+'
            patch = patch + 'Code'
        df.at[i, 'patch_loc'] = patch
    df2 = df.drop(['reproduce_successes', '_updated', 'changes', 'deletions', 'additions', 'repo_commits', 'repo', 'reproduced', 'tag', 'creation_time', 'passed_job', 'failed_job', 'repo_builds', 'status_time_stamp', 'is_error_pass', 'repo_prs', 'pr_num','stability', 'reproduce_attempts', 'build', 'code', 'test'], axis = 1, inplace=False)
    pivot = df2.pivot_table( values='exceptions', index=['lang', 'os', 'patch_loc', 'status', 'test_framework'], columns='build_system', aggfunc='count', fill_value=0)
    pivot_dict = pivot.to_dict('index')
    dat = []
    for key in pivot_dict:
        iterDat = dat
        for i in range(len(key)):
            found = False
            foundDat = None
            for d in iterDat:
                if d['name'] == key[i]:
                    found = True
                    foundDat = d
                    break
            if not found:
                foundDat = {}
                foundDat['name'] = key[i]
                foundDat['children'] = []
                iterDat.append(foundDat)
            iterDat = foundDat['children']

            if i == len(key) - 1:
                val = pivot_dict[key]
                for leaf in val:
                    foundChild = False
                    foundChildLeaf = None
                    for child in iterDat:
                        if child['name'] == leaf:
                            foundChild = True
                            foundChildLeaf = child
                            break
                    if not foundChild:
                        newChild = {}
                        newChild['name'] = leaf
                        newChild['value'] = val[leaf]
                        iterDat.append(newChild)
                    else:
                        foundChildLeaf['value'] = foundChildLeaf['value'] + val[leaf]
            
    return dat
    

if __name__ == "__main__":
	app.run(debug=True)
