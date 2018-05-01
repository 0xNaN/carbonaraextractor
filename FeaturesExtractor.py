import numpy as np

class FeaturesExtractor():
    def extract(self, node, selected=[], features_descriptor={}):
        features = {}
        for name in selected:
            features[name] = features_descriptor[name](node)
        return features

    def toArray(self, features):
        features_sorted_by_name = sorted(features.items(), key=lambda f:f[0])
        features_values = list(map(lambda f:f[1], features_sorted_by_name))
        features_array = np.fromiter(features_values, np.float32)
        return features_array
