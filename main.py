import sys
import requests

import lxml.html as lx

from DomUtils import *
from CarbonaraBros import *

def node_text_summary(node, chars=None):
    words = DomUtils.node_words(node)
    text = " ".join(words)
    if type(chars) == int:
        return text[:chars]
    return text

if __name__ == '__main__':
    url = sys.argv[1]

    dom = domFromUrl(url, dump_on="working.html")
    carbonara = CarbonaraBros(relevant_threshold=0.8)

    analysis = carbonara.processDom(dom)
    tables = analysis['table']

    print()
    print("RELEVANT FOUND: {}".format(len(tables['relevant'])))
    for score, node in tables['relevant']:
        print(">> {}".format(score))
        print(node_text_summary(node, chars=200))

    print()
    print("NOT RELEVANT FOUND: {}".format(len(tables['not_relevant'])))
    for score, node in tables['not_relevant']:
        print(">>> {}".format(score))
        print(node_text_summary(node, chars=100))
