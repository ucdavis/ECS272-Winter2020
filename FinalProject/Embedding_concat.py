#!/usr/bin/env python
# coding: utf-8

# In[19]:


import pandas as pd
import numpy as np


# In[20]:


def concat_embeddings(input_df, embedding1_wt, embedding2_wt, embedding3_wt ):
    weighted1 = []
    weighted2 = []
    weighted3 = []
    
    for item in input_df.embedding1.tolist():
        weighted1.append(list(map(lambda x: x*embedding1_wt, item)))
    #print(input_df.embedding1.tolist())
    #print(weighted1)
    for item in input_df.embedding2.tolist():
        weighted2.append(list(map(lambda x: x*embedding2_wt, item)))
    #print(input_df.embedding2.tolist())
    #print(weighted2)
    for item in input_df.embedding3.tolist():
        weighted3.append(list(map(lambda x: x*embedding3_wt, item)))
    
    for i in range(len(weighted1)):
        weighted1[i] += weighted2[i] + weighted3[i]         
    
    #print(weighted1)
    
    input_df['concat_embedding'] = weighted1


# # Rough Callback

# In[ ]:


@app.callback(
        [Output('chart', 'figure')],
        [Input('wt1_slider', 'value'),
        Input('wt2_slider', 'value'),
        Input('wt3_slider', 'value')]
    )
    def update_radar_chart(wt1, wt2, wt3):
        concat_embeddings(df, wt1, wt2, wt3)
        # update figure for chart with data from df


# # Test

# In[21]:


rows2 = []
dict93 = {
    "embedding1" : [0,2,3,5,7],
    "embedding2" : [0,2,3,5,7],
    "embedding3" : [0,2,3,5,7]
    
}
rows2.append(dict93)
dict94 = {
    "embedding1" : [0,1,2,3,4],
    "embedding2" : [0,2,3,5,7],
    "embedding3" : [0,2,3,5,7]
}
rows2.append(dict94)
test_df = pd.DataFrame(rows2)

concat_embeddings(test_df, 2, 3, 1)
test_df

