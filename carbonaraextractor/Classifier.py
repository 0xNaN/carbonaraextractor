import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=FutureWarning)
    import keras
import numpy as np
import pickle as pkl

class Classifier():

    def __init__(self, model_path, scaler_path):
        self.model = keras.models.load_model(model_path)
        self.scaler = pkl.load(open(scaler_path, "br"))

    def classify(self, features_array):
        features_single_batch = features_array.reshape((1, len(features_array)))
        features_single_batch = self.scaler.transform(features_single_batch)

        batch_result = self.model.predict(features_single_batch)

        return batch_result[0]
