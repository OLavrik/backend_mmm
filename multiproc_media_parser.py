#!/usr/bin/env python
import os
import multiprocessing as mp
from ClassHMM.class_model import MediaParser
import argparse

def parse_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('target_dir')
    parser.add_argument('-o', '--outdir', required=True)
    parser.add_argument('-p', '--processes', type=int, required=False, default=4)
    return parser.parse_args()


def process_folder(dump_dir, task_que, print_lock, ID):
    while True:
        try:
            cur_dir = task_que.get(block=True, timeout=5)
        except:
            with print_lock:
                print(f'Closing process {ID}')
            break

        with print_lock:
            print(f'{ID:<2}: Processing {cur_dir}')

        dir_objects = [os.path.join(cur_dir, o) for o in os.listdir(cur_dir)]

        subfolsers = [dir_ for dir_ in dir_objects if os.path.isdir(dir_)]
        mp3_files = [mp3f for mp3f in dir_objects if os.path.isfile(mp3f) and mp3f.endswith('.mp3')]

        # first, push all files to QUEUE
        for sf in subfolsers:
            task_que.put_nowait(sf)

        if len(subfolsers) > 0:
            with print_lock:
                print(f'{ID:<2}: Added {len(subfolsers)} items to queue')

        try:
            # Create DF for current folder
            m = MediaParser()
            m.files_generator = mp3_files
            df = m.construct_df()
            df_pickle_name = os.path.basename(cur_dir.rstrip('/'))+'.pkl'
            df.to_pickle(os.path.join(dump_dir, df_pickle_name))
        except Exception as e:
            with print_lock:
                print(f'{ID:<2}: FAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIL {cur_dir} {e}')
        else:
            with print_lock:
                print(f'{ID:<2}: Wrote dataframe {df_pickle_name}')


if __name__ == '__main__':
    args = parse_cli()

    ctx = mp.get_context()
    task_que = ctx.Queue()
    task_que.put(args.target_dir)
    print_lock = mp.Lock()
    PROCESS_CNT = 4
    dump_dir = os.path.abspath(args.outdir)
    os.makedirs(dump_dir, exist_ok=True)
    os.makedirs('tmp', exist_ok=True)
    prc_list = [ctx.Process(target=process_folder, args=(dump_dir, task_que, print_lock, i)) for i in range(args.processes)]


    for prc in prc_list:
        prc.start()

    #prc_list[0].join()