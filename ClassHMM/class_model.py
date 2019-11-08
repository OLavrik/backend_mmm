import wave
from pydub import AudioSegment
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import csv
import librosa
from librosa.feature import mfcc
import sklearn.preprocessing
import os
import glob
import uuid
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings("ignore")

class MediaParser:
    def __init__(self, root_dir='/'):
        self.root_dir = root_dir
        self.scale = True
        self.nmfcc = 20
        self.nfft = 512
        self.hop_length = 512
        self.names_list = []
        self.tempfilename = uuid.uuid4()
        self.files_generator = None

    def ap(self, file):
        # ap stands for Absolute Path
        return os.path.join(self.root_dir, file)

    def recursive_deep_generator(self):
        for root, dirs, files in os.walk(self.root_dir):
            for name in files:
                if name.endswith('.mp3'):
                    yield self.ap(os.path.join(root, name))

    def wav_audio_generator(self):
        for mp3_path in self.files_generator:
            sound = AudioSegment.from_mp3(mp3_path)
            sound.export(os.path.join('tmp',str(self.tempfilename)), format="wav")
            yield os.path.basename(mp3_path)

    def feature_extractor_generator(self):
        for name in self.wav_audio_generator():
            audio, s_freq = librosa.load(os.path.join('tmp', str(self.tempfilename)), sr=None, res_type='scipy')
            features = librosa.feature.mfcc(audio, s_freq, n_mfcc=self.nmfcc, n_fft=self.nfft,
                                            hop_length=self.hop_length)
            features = sklearn.preprocessing.scale(features)[1]
            if len(features) > 10000:
                features = features[:10000]
            else:
                features = np.pad(features, (0, 10000 - len(features)), 'constant', constant_values=(0, 0))
            # print(f'Processed: {name}')
            self.names_list.append(name)
            yield features

    def construct_df(self):
        gen = self.feature_extractor_generator()
        df = pd.DataFrame(gen)
        df['song'] = self.names_list
        df.set_index('song', inplace=True)
        return df


def construct_for_each_subfolder(root_dir):
    subdolsers = [os.path.join(root_dir, o) for o in os.listdir(root_dir)
                if os.path.isdir(os.path.join(root_dir, o))]
    for sf in subdolsers:
        print(f'Creating DF for: {sf}')
        m = MediaParser(sf)
        m.files_generator = m.recursive_deep_generator
        df = m.construct_df()
        df.to_pickle(os.path.basename(sf.rstrip('/'))+'.pkl')
        print(str(df))
        del m



class Model:
    def __init__(self, path):
        self.nfft = 512
        self.nmfcc = 20
        self.hop_length = 512
        self.res_type = 'scipy'
        self.scale = True
        self.path = path

    def from_mp3_to_wan(self):
        for file in glob.glob(self.path + "/*.mp3"):
            sound = AudioSegment.from_mp3(file)
            sound.export(str(file).split('.')[0] + '.wav', format="wav")

    def getFeaturesFromWAV(self, filename):
        # разобраться что load возвращает
        self.audio, self.sampling_freq = librosa.load(
            filename, sr=None, res_type=self.res_type)
        self.features = librosa.feature.mfcc(
            self.audio, self.sampling_freq, n_mfcc=self.nmfcc, n_fft=self.nfft, hop_length=self.hop_length)
        if self.scale:
            self.features = sklearn.preprocessing.scale(self.features)
        a = np.zeros(10000)
        for i in range(10000):
            a[i] = self.features[1][i]
        return a

    def make_features(self):
        listf = []
        for file in glob.glob(self.path + "/*.wav"):
            listf.append(self.getFeaturesFromWAV(file))
        self.list_features = np.asarray(listf)

    def model_knn(self):
        self.model = KMeans(n_clusters=2)
        self.model.fit(self.list_features)

    def model_predict(self, list_filename):
        listF = []
        for filename in list_filename:
            listF.append(self.getFeaturesFromWAV(filename))

        res = self.model.predict(listF)

        list_1 = []
        list_2 = []
        for i in range(len(res)):
            if res[i] == 0:
                list_1.append(list_filename[i])
            if res[i] == 1:
                list_2.append(list_filename[i])
        return list_1, list_2

if __name__ == '__main__':
    construct_for_each_subfolder('/media/E/Nikita/Music/_VK')