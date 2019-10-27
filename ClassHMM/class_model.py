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
from sklearn.cluster import KMeans


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
            filename, sr=None, res_type=res_type)
        self.features = librosa.feature.mfcc(
            self.audio, self.sampling_freq, n_mfcc=self.nmfcc, n_fft=self.nfft, hop_length=self.hop_length)
        if scale:
            self.features = sklearn.preprocessing.scale(self.features)
        a = np.zeros(10000)
        for i in range(10000):
            a[i] = features[1][i]
        return a

    def make_features(self):
        listf = []
        for file in glob.glob("music/*.wav"):
            listf.append(getFeaturesFromWAV(file))
        self.list_features = np.asarray(listf)

    def model_knn(self):
        self.model = KMeans(n_clusters=2)
        self.model.fit(self.list_features)

    def model_predict(self, list_filename):
        listF = []
        for filename in list_filename:
            listF.append(getFeaturesFromWAV(filename))

        res = model.predict(listF)

        list_1 = []
        list_2 = []
        for i in range(len(res)):
            if res[i] == 0:
                list_1.append(list_filename[i])
            if res[i] == 1:
                list_2.append(list_filename[i])
        return list_1, list_2
