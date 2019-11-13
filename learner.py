#!/usr/bin/env python
import os
import pickle
import argparse
import pandas as pd

import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def parse_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('pickled_df')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_cli()

    df_songs = pd.read_pickle(args.pickled_df)
    df_np = df_songs.reset_index(drop=True).values
    print(df_np.shape)

    # fit

    # predict


    K = range(2, 15)
    models = []
    for n_clus in K:
        print('-------------------------------------------------------------')
        print('Fitting', n_clus)
        print('-------------------------------------------------------------')
        models.append(KMeans(n_clusters=n_clus, random_state=42, verbose=1).fit(df_np))

    with open('all_models.pkl', 'wb') as f:
        pickle.dump(models,f)
    dist = [model.inertia_ for model in models]

    # Plot the elbow
    plt.plot(K, dist, marker='o')
    plt.xlabel('k')
    plt.ylabel('Sum of distances')
    plt.title('The Elbow Method showing the optimal k')
    plt.show()

