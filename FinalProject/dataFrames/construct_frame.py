#making my data frame

import pandas as pd
from PIL import Image

possible_keywords = ['average','G3', 'absences', 'address', 'age', 'bar chart', 'box and whisker', 'box and whisker plot', 'categorical', 'compare', 'continuous', 'correlation', 'correlation coefficients', 'count', 'discrete', 'distribution', 'facetgrid', 'grades', 'health', 'heatmap', 'higher', 'histogram', 'internet', 'multiple bars', 'multiple charts', 'multiple plots', 'numerical', 'romantic', 'sex', 'st_time', 'traveltime', 'two charts', 'two columns']
possible_features = ['school', 'sex', 'age', 'address', 'famsize', 'Pstatus', 'Medu', 'Fedu', 'Mjob', 'Fjob', 'reason', 'guardian', 'traveltime', 'studytime', 'failures', 'schoolsup', 'famsup', 'paid', 'activities', 'nursery', 'higher', 'internet', 'romantic', 'famrel', 'freetime', 'goout', 'Dalc', 'Walc', 'health', 'absences', 'G1', 'G2', 'G3']
df_columns        = ['image', 'title', 'author', 'keywords', 'features', 'code']

def append_frame(im, title, author, keywords, features, code, df = None):
    
    global possible_keywords
    global possible_features
    global df_columns
    
    #check keywords and features
    for word in keywords:
        if not (word in possible_keywords):
            raise ValueError(word + " not in keywords")
    for feat in features:
        if not (feat in possible_features):
            raise ValueError(feat + " not in features")
    
    #make single row dataframe of this data
    new_df = pd.DataFrame([[im, title, author, keywords, features, code]], columns = df_columns)
    
    #append new_df to df, if provided
    if df is None:
        df = new_df
    else:
        df = pd.concat((df, new_df), axis = 0)
    
    df.reset_index(drop = True, inplace = True)
    return df


############## EXAMPLE ##############

##kernel 3
#author = "Balagyozyan"
#
##chart 1
##image saved as png to local directory
#im = Image.open("graph_images/kernel_3_c_1.png")
##im.show()
#
#title = ''
#keywords = ['correlation','discrete','grades','two charts']
#features = ['G1','G2','G3','Dalc','Walc']
#code = "grid.arrange(str1,str2,nrow=2)"
#
#df = append_frame(im, title, author, keywords, features, code, None)
#
##chart 2
#im = Image.open("graph_images/kernel_3_c_2.png")
#
#title = 'Average Grade'
#keywords = ['average','grades','box and whisker']
#features = ['G1','G2','G3','Dalc']
#code = "ggplot(d3norepeats, aes(x=Dalc, y=avggrades, group=Dalc))+geom_boxplot()+theme(legend.position=\"none\")+scale_fill_manual(values=waffle.col)+xlab(\"Daily Alcohol consumption\")+ylab(\"Average Grades\")+ggtitle(\"Average Grade\")"
#
#df = append_frame(im, title, author, keywords, features, code, df)
#
##save dataframe with pickle
#pd.to_pickle(df,"mjlyons7_df")
