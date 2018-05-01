import sys
import requests
import json
import re
import numpy as np

import lxml.html as lx

from DomUtils import *
from CarbonaraBros import *
from FeaturesExtractor import *

def node_text_summary(node, length=50):
    words = [n.text_content().strip() for n in node.xpath(".//*[not(*)]")]
    text = " ".join(words).strip()
    text = re.sub(r"\W+", " ", text)
    return text[:length]

# XXX:
# node must have at least two children.
# the first will be the key, the others the value
#
# what about
# <tr>
#   my key: <b> my value </b>
# </tr>
#
# or
# <tr>
#   <b>my key:</b>  my value
# </tr>
# ??
def node_to_key_value(node):
    key = value = None

    while len(node.getchildren()) == 1:
        node = node.getchildren()[0]

    children = node.getchildren()

    if len(children) == 0:
        raise EmptyNode

    key = children[0].text_content()
    key = re.sub(r' +', " ", key).strip()

    children.pop(0)
    value = " ".join(map(lambda n: n.text_content().strip(), children))
    value = re.sub(r' +', " ", value).strip()

    return (key, value)

def append_key_value_to_dict(dict, key, value):
    if key not in dict:
        dict[key] = value
        return

    if type(dict[key] != list):
        dict[key] = [dict[key]]

    dict[key].append(value)

def analysis_to_dict(analysis):
    ret = {
        '__unstructured': []
    }

    # table
    relevant_tr = [table.xpath(".//tr") for _, table in analysis['table']['relevant']]
    relevant_tr = set([tr for list_of_tr in relevant_tr for tr in list_of_tr])
    for tr in relevant_tr:
        try:
            key, value = node_to_key_value(tr)
            append_key_value_to_dict(ret, key, value)
        except:
            print(">>>> tr skipped")

    # list
    # XXX: mancano i dt (che non hanno i li)
    # bisogna anche eliminare dal dom tutto ciò che è stato processato, altrimenti
    # si analizza più volte lo stesso contenuto?
    # es: https://www.gearbest.com/action-cameras/pp_651543.html?wid=4
    # <dd> che contiene <ul>
    relevant_li = [list.xpath(".//li") for _, list in analysis['list']['relevant']]
    relevant_li = set([li for list_of_li in relevant_li for li in list_of_li])

    for li in relevant_li:
        try:
            key, value = node_to_key_value(li)
            append_key_value_to_dict(ret, key, value)
        except:
            ret['__unstructured'].append(li.text_content().strip())

    return ret

def with_color(msg, color="green"):
    end = '\033[0m'
    colorCode = ""

    if   color == "green":
        colorCode = '\033[92m'
    elif color == "red":
        colorCode = '\033[91m'
    elif color == "blue":
        colorCode = '\033[94m'

    return colorCode + str(msg) + end

def print_result(result, color):
    for score, node in result:

        # 1° column: score
        score = round(score, 2)

        # 2° column: text d
        summary_length = 60
        node_summary = node_text_summary(node, length=summary_length)
        node_summary = '"{}"'.format(node_summary)

        # 3° column: feature vector
        descriptor = DefaultFeatures.table if node.tag == "table" else DefaultFeatures.list
        selected   = DefaultFeatures.table_selected if node.tag == "table" else DefaultFeatures.list_selected
        ft = FeaturesExtractor()
        features = ft.extract(node, selected=selected, features_descriptor=descriptor)
        features_array = ft.toArray(features)

        padding = " " * (summary_length - len(node_summary))

        print(with_color(score, color=color),
              node_summary,
              padding,
              str(list(features_array)))

if __name__ == '__main__':
    url = sys.argv[1]

    dom = domFromUrl(url, dump_on="working.html")
    carbonara = CarbonaraBros(relevant_threshold=0.8)

    analysis = carbonara.processDom(dom)

    print(with_color("TABLES", color="blue"))
    print_result(analysis['table']['relevant'], color="green")
    print_result(analysis['table']['not_relevant'], color="red")

    print(with_color("\nLIST", color="blue"))
    print_result(analysis['list']['relevant'], color="green")
    print_result(analysis['list']['not_relevant'], color="red")

    result = analysis_to_dict(analysis)

    with open('result.json', 'w') as fp:
        json.dump(result, fp, indent=2)
