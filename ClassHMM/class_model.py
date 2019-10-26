
class Model:
    def __init__(self,path):
        self.nfft = 512
        self.nmfcc = 20
        self.hop_length = 512
        self.res_type = 'scipy'
        self.scale = True
        self.path=path



    def getFeaturesFromWAV(self,filename):
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

    def model_predict(self,filename):
        self.model(list1.append(getFeaturesFromWAV(filename)))

