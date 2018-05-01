import numpy as np
import keras

class Classifier():

    def __init__(self, model_path):
        self.model = keras.models.load_model(model_path)

    def classify(self, features_array):
        features_single_batch = features_array.reshape((1, len(features_array)))

        batch_result = self.model.predict(features_single_batch)

        return batch_result[0]
