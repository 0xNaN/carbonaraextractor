class FeaturesExtractor():
    def extract(self, node, features_descriptor={}):
        features = {}
        for name in features_descriptor:
            features[name] = features_descriptor[name](node)
        return features
