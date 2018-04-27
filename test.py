import sys
import lxml.html as lx

from DomUtils import *
from CarbonaraBros import *

import pandas

if len(sys.argv) < 2:
    print("""
    usage:
        python test.py <filepath_site_goldenxpath>
    """)
    exit(1)

test_suite_path = sys.argv[1]
test_suite = pandas.read_csv(test_suite_path, header=None, sep="\t")

carbonara = CarbonaraBros()

for _, row in test_suite.iterrows():
    url = row[0]
    golden_xpath = row[1]

    dom = domFromUrl(url)
    analysis = carbonara.processDom(dom)

    our_relevants     = set(map(lambda x: x[1], analysis['table']['relevant']))
    our_not_relevants = set(map(lambda x: x[1], analysis['table']['not_relevant']))
    true_relevants    = set(dom.xpath(golden_xpath))

    true_positive  = our_relevants.intersection(true_relevants)

    print(url)
    print("{}/{} (relevants {}/{})".format(len(true_positive), len(true_relevants),
                                           len(our_relevants), (len(our_relevants) + len(our_not_relevants))))
