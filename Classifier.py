import numpy as np
import keras

class Classifier():

    def __init__(self, model_path):
        self.model = keras.models.load_model(model_path)

    def classify(self, features):
        # XXX: input array ordered by feature name
        features_sorted_by_name = sorted(features.items(), key=lambda f:f[0])
        features_values = list(map(lambda f:f[1], features_sorted_by_name))

        features_array = np.fromiter(features_values, np.int)
        features_single_batch = features_array.reshape((1, len(features_array)))

        batch_result = self.model.predict(features_single_batch)

        return batch_result[0]
