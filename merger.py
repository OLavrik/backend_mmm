import os
import argparse
import pandas as pd

def parse_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('target_dir')
    parser.add_argument('-o', '--outdir', required=True)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_cli()
    pickles = [os.path.join(args.target_dir,f) for f in os.listdir(args.target_dir) if f.endswith('.pkl')]

    dfs = [pd.read_pickle(pick) for pick in pickles]

    res_df=pd.concat(dfs, copy=False)

    print(res_df)

    res_df.to_pickle('_result.pkl')

