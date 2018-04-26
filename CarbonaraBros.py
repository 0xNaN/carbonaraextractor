import sys
import requests
import lxml.html as lx
import nltk
import re

import DefaultFeatures
from FeaturesExtractor import *
from Classifier import *



def domFromUrl(url, dump_on=""):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
    }

    r = requests.get(url, headers=headers)

    if dump_on != "":
        with open(dump_on, "w") as d:
            d.write(r.text)

    return lx.fromstring(r.text)

def node_text_summary(node, chars=None):
    text = node.text_content()
    text = text.strip()
    text = re.sub(r'\s+', " ", text)

    if type(chars) == int:
        return text[:chars]
    return text

if __name__ == '__main__':
    print()
    fe = FeaturesExtractor()

    url = sys.argv[1]
    dom = domFromUrl(url, dump_on="working.html")

    # table
    tableClassifier = Classifier('models/table_classifier.h5')

    for table in dom.xpath("//table"):
        features = fe.extract(table, features_descriptor=DefaultFeatures.table)
        r = tableClassifier.classify(features)

        if (r[0] >= 0.8):
            print(">> relevant found {}".format(r[0]))
            print(node_text_summary(table))
            print()
        else:
            print(">> skipped {}".format(r[0]))
            print(node_text_summary(table, chars=100))
