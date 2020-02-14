from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
import json
import pandas as pd
from sklearn.cluster import KMeans
import os
from Assignment4 import settings

# Create your views here.


def __test__(request):
    return render(request, 'visualization.html')

def cluster(request):
    if request.is_ajax():
        df = pd.read_csv(os.path.join(settings.BASE_DIR, 'pokemon_alopez247.csv'))
        filtered = df.loc[:, ['Attack', 'Defense']]
        ret = {}
        data = []
        for i in range(len(filtered)):
            data.append([filtered['Attack'][i], filtered['Defense'][i]])
        kmeans = None
        if request.method == 'POST':
            kmeans = KMeans(n_clusters=int(request.POST['k'])).fit(data)
            ret['K'] = int(request.POST['k'])
        elif request.method == 'GET':
            kmeans = KMeans(n_clusters=4).fit(data)
            ret['K'] = 4
        filtered['Cluster'] = kmeans.labels_
        ret['Attack'] = list(filtered['Attack'])
        ret['Defense'] = list(filtered['Defense'])
        ret['Id'] = list(df['Number'])
        ret['Name'] = list(df['Name'])
        ret['Total'] = list(df['Total'])
        ret['Generation'] = list(df['Generation'])
        ret['hasGender'] = list(df['hasGender'])
        ret['Cluster'] = list(filtered['Cluster'])
        ret['Speed'] = list(df['Speed'])
        return JsonResponse(ret)
    else:
        raise Http404

def sankey(request):
    if request.is_ajax():
        df = pd.read_csv(os.path.join(
            settings.BASE_DIR, 'pokemon_alopez247.csv'))
        columns = ['Type_1', 'Generation', 'Color', 'Body_Style']
        filtered = df.loc[:, columns]
        filtered = filtered.fillna('None')
        nodes = []
        nodes_ = []
        for i in range(len(columns)):
            if columns[i] == 'Generation':
                uni = [int(v) for v in list(filtered[columns[i]].unique())]
                nodes.append(uni)
                for key in uni:
                    nodes_.append({
                        'id': key
                    })
                continue
            uni = list(filtered[columns[i]].unique())
            nodes.append(uni)
            for key in uni:
                nodes_.append({
                    'id': key
                })

        links = []
        for i in range(len(columns)-1):
            sources = nodes[i]
            targets = nodes[i+1]
            for j in range(len(nodes[i])):
                for k in range(len(nodes[i+1])):
                    links.append({
                        'source': nodes[i][j],
                        'target': nodes[i+1][k],
                        'value': len(filtered.loc[(filtered[columns[i]] == nodes[i][j]) & (filtered[columns[i+1]] == nodes[i+1][k])])
                    })

        ret = {'nodes': nodes_, 'links': links}
        #print(ret)
        return JsonResponse(ret)
    else:
        raise Http404


def histogram(request):
    if request.is_ajax():
        df = pd.read_csv(os.path.join(
            settings.BASE_DIR, 'pokemon_alopez247.csv'))
        x = [int(v) for v in df['Speed']]
        ret = {'x': x}
        return JsonResponse(ret)
    else:
        raise Http404
