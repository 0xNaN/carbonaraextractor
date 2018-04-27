class FeaturesExtractor():
    def extract(self, node, selected=[], features_descriptor={}):
        features = {}
        for name in selected:
            features[name] = features_descriptor[name](node)
        return features
