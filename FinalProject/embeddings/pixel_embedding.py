import pandas as pd
import numpy as np

'''
In: the dataFrame containing the entire dataset of chart images

Out: the dataFrame containing the entire dataset of chart images with
a new column of "pixel_embeddings"

resizes each image in the dataFrame to be 100x100 pixels, converts to
grayscale so the shape is 100x100x1, flattens to an array of length
10000, normalizes all the elements so they are in the range [0,1],
saves this as a "pixel_embedding"
'''
def generate_pixel_embeddings(df):
    df["pixel_embedding"] = df.apply(lambda x : np.array(x.image.resize((100,100)).convert("L")).flatten()/255, axis=1)
    return df