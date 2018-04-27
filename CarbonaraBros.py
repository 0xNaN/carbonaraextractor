import DomUtils
import DefaultFeatures
from FeaturesExtractor import *
from Classifier import *

class CarbonaraBros():

    def __init__(self, relevant_threshold = 0.8):
        self.fe = FeaturesExtractor()
        self.relevant_threshold = relevant_threshold
        self.tableClassifier =  Classifier('models/table_classifier.h5')

    def processDom(self, dom):
        analysis = {
            'table': {
                'relevant': [],
                'not_relevant': []
            }
        }

        # table
        for table in dom.xpath("//table"):
            features = self.fe.extract(table, selected = DefaultFeatures.table_selected,
                                              features_descriptor = DefaultFeatures.table)
            score = self.tableClassifier.classify(features)
            score = score[0]

            if score >= self.relevant_threshold:
                analysis['table']['relevant'].append((score, table))
            else:
                analysis['table']['not_relevant'].append((score, table))

        return analysis
