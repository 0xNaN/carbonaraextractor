import sys
import lxml.html as lx

from DomUtils import *
from CarbonaraBros import *

import pandas

def apply_xpaths(node, xpaths):
    nodes = set()
    for xpath in xpaths:
        for node in node.xpath(xpath):
            nodes.add(node)
    return nodes

if len(sys.argv) < 2:
    print("""
    usage:
        python test.py <filepath_site_goldenxpath>
    """)
    exit(1)

test_suite_path = sys.argv[1]
test_suite = pandas.read_csv(test_suite_path, header=None, sep="\t")
test_suite = test_suite.groupby(0)[1].apply(list)

carbonara = CarbonaraBros()

print("URL\t\t\tTP\tFP\tTN\tFN")

for url, golden_xpaths in test_suite.iteritems():
    dom = domFromUrl(url)

    analysis = carbonara.processDom(dom)
    our_relevants     = set(map(lambda x: x[1], analysis['table']['relevant']))
    our_not_relevants = set(map(lambda x: x[1], analysis['table']['not_relevant']))

    true_relevants = apply_xpaths(dom, golden_xpaths)

    tp = len(our_relevants.intersection(true_relevants))
    fp = len(our_relevants.symmetric_difference(true_relevants))
    tn = len(our_not_relevants.symmetric_difference(true_relevants))
    fn = len(our_not_relevants.intersection(true_relevants))

    print("{}\t\t\t{}\t{}\t{}\t{}".format(url, fp, fp, tn, fn))
