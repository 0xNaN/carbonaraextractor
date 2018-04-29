import sys
import requests
import json

import lxml.html as lx

from DomUtils import *
from CarbonaraBros import *

def node_text_summary(node, chars=None):
    words = DomUtils.node_stems(node)
    text = " ".join(words)
    if type(chars) == int:
        return text[:chars]
    return text

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

    key = children[0].text_content().strip()

    children.pop(0)
    value = " ".join(map(lambda n: n.text_content().strip(), children))

    return (key, value)

def analysis_to_dict(analysis):
    ret = {}

    # table
    tr_done = set()
    for _, table in analysis['table']['relevant']:
        for tr in table.xpath(".//tr"):
            if tr not in tr_done:
                tr_done.add(tr)

                try:
                    key, value = node_to_key_value(tr)
                    if key not in ret:
                        ret[key] = value
                    else:
                        if type(ret[key]) == list:
                            ret[key].append(value)
                        else:
                            ret[key] = [ret[key], value]
                except:
                    print(">> tr skipped")

    return ret


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

#    print()
#    print("CHILDREN OF RELEVANT FOUND: {}".format(len(tables['children_of_relevant'])))
#    for score, node in tables['children_of_relevant']:
#        print(">> {}".format(score))
#        print(node_text_summary(node, chars=200))


    print()
    print("NOT RELEVANT FOUND: {}".format(len(tables['not_relevant'])))
    for score, node in tables['not_relevant']:
        print(">>> {}".format(score))
        print(node_text_summary(node, chars=100))

    result = analysis_to_dict(analysis)

    with open('result.json', 'w') as fp:
        json.dump(result, fp, indent=2)
