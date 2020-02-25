from typing import List, Sequence
import pandas as pd
import sklearn
import sklearn.manifold
from pandas import DataFrame
from sklearn import preprocessing
from data_constants import feats_numeric, feats_ordinal, feats_categorical, feats_bool, feats_all
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, MinMaxScaler


def load_data():
    return pd.read_csv("./data/pokemon_alopez247.csv")


def vectorize_examples(df: DataFrame, accepted_cols: List[str] = None, normalize: bool = False):
    """Converts the pokemon dataset to feature vectors

    :arg df: The data from our pokemon dataset
    :arg accepted_cols: if provided, only these columns will be considered
    :arg normalize: If true will output feature vectors scaled to be unitnorm
    """
    if accepted_cols:
        assert all([feat in feats_all for feat in accepted_cols])

    def filter_feats(feats: Sequence[str]):
        if accepted_cols is None:
            return feats
        return [feat for feat in feats if feat in accepted_cols]

    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler())])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))])

    bool_transformer = Pipeline(steps=[
        ('encoder', MinMaxScaler())]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, filter_feats(feats_numeric + feats_ordinal)),
            ('cat', categorical_transformer, filter_feats(feats_categorical)),
            ('bool', bool_transformer, filter_feats(feats_bool))
        ]
    )
    preprocessor.fit_transform(df)
    vecs = preprocessor.transform(df)
    if normalize:
        vecs = preprocessing.normalize(vecs)
    return vecs


def run_tsne(features):
    tsne = sklearn.manifold.TSNE(n_components=2, random_state=42)
    tsne.fit_transform(features)
    return tsne.embedding_


if __name__ == "__main__":
    # Make sure we can load the data [DONE]
    # Hello dash [DONE]
    # Dim reduction
    #   Map the pokemon to a vector [DONE]
    #   Run dim reduction [DONE]
    #   Show in dash [DONE]
    #   Paramertized dim reduction
    #       Show the multi selection
    #       Redo dim reduction when changing the parameters
    # Show stats bar graph [DONE]
    # Figure out how to link stats bargraph and scatter plot of dim reduction [DONE]
    # Be able to show table of things in given filter
    # Sankey
    #   Draw the sankey
    #   Extra interaction??
    # (Optional) figure out picture in table

    df = load_data()
    #subdf = df
    #sub_fields = ['HP', 'Type_1', 'hasGender', 'Height_m']
    #print(subdf[sub_fields])
    vectroized = vectorize_examples(df, None)
    print(vectroized)
    print(vectroized.shape)
    print("RUN tsne")
    tsne = run_tsne(vectroized)
    print(tsne)


