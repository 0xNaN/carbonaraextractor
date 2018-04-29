import DomUtils
import DefaultFeatures

from DomUtils import *
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
#                'children_of_relevant': [],
                'not_relevant': [],
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

#        children_of_relevant = []
#        for score, node_not_relevant in analysis['table']['not_relevant']:
#            if child_of_any(node_not_relevant, analysis['table']['relevant']):
#                children_of_relevant.append((score, node_not_relevant))
#
#        analysis['table']['not_relevant'] = [node for node in analysis['table']['not_relevant'] if node not in children_of_relevant]
#        analysis['table']['children_of_relevant'] = children_of_relevant

        return analysis

