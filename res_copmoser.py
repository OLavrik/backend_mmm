#!/usr/bin/env python
import os
import pickle
import argparse
import pandas as pd

import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def parse_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', type=str)
    parser.add_argument('pickled_df', type=str)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_cli()

    with open(args.model, 'rb') as f:
        mdl = pickle.load(f)

    df_songs = pd.read_pickle(args.pickled_df)

    print(df_songs)
    print(mdl)

    names = df_songs.index.to_series()
    names.reset_index(drop=True, inplace=True)

    labels = pd.Series(mdl.labels_)
    frame = {'Label': labels, 'Name': names}

    res = pd.DataFrame(frame)
    res.set_index(['Label', res.index],inplace=True)
    res.sort_index(inplace=True)
    res.reset_index(0, inplace=True)
    print(res)
    res.to_csv('result_41.csv', index=False)