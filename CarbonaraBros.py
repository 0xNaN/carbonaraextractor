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
        self.listClassifier =  Classifier('models/list_classifier.h5')

    def processDom(self, dom):
        analysis = {
            'table': {
                'relevant': [],
                'not_relevant': [],
            },
            'list': {
                'relevant': [],
                'not_relevant': []
            }
        }

        # table
        for table in dom.xpath("//table"):
            features = self.fe.extract(table, selected = DefaultFeatures.table_selected,
                                              features_descriptor = DefaultFeatures.table)
            features_array = self.fe.toArray(features)
            score = self.tableClassifier.classify(features_array)
            score = score[0]

            if score >= self.relevant_threshold:
                analysis['table']['relevant'].append((score, table))
            else:
                analysis['table']['not_relevant'].append((score, table))


        lists = dom.xpath("//ul")
        lists = lists + dom.xpath("//ol")
        lists = lists + dom.xpath("//dl")

        for list in lists:
            features = self.fe.extract(list, selected = DefaultFeatures.list_selected,
                                              features_descriptor = DefaultFeatures.list)
            features_array = self.fe.toArray(features)
            score = self.listClassifier.classify(features_array)
            score = score[0]

            if score >= self.relevant_threshold:
                analysis['list']['relevant'].append((score, list))
            else:
                analysis['list']['not_relevant'].append((score, list))

        return analysis

