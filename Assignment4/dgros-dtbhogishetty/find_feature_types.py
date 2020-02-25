"""Simple scripts for exploring the coloumns of our data"""
from data_constants import feats_all
from dataproc import load_data


if __name__ == "__main__":
    df = load_data()
    print(df.columns)
    print(set(list(df['Body_Style'])))
    for col in df.columns:
        print(col)
        print("NUM UNIQUE", df[col].nunique(dropna=False))
        print(df[col].sample(n=10))
    for feat in feats_all:
        assert feat in df.columns

