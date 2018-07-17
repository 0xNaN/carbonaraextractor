import nltk
import requests
import re
import lxml.html as lx

def count_xpath(node, xpath):
    return len(node.xpath(xpath))

def count_stem(node, stems, sep=" "):
    return len(stems.intersection(node_stems(node)))

def depth(node):
    max_depth = 0
    leaves = node.xpath(".//*[not(*)]")

    for leave in leaves:
        max_depth = max(max_depth, count_between(leave, node))

    return max_depth

def count_between(start_node, stop_node):
    parents = 0
    while (start_node is not stop_node) and (start_node != None) :
        start_node = start_node.getparent()
        parents += 1
    return parents

def node_stems(node):
    text = " ".join(node.itertext())
    text = re.sub(r"[^a-z0-9]", " ", text, flags=re.IGNORECASE)

    porter = nltk.stem.PorterStemmer()
    stems = map(porter.stem, re.split(r'\W+', text))

    return set(stems)

def child_of_any(node, nodes):
    for n in nodes:
        if count_between(node, n) > 0:
            return True
    return False

def domFromUrl(url, dump_on=""):
    req = requests.get(url)
    source = req.content

    if dump_on != "":
        with open(dump_on, "w") as d:
            d.write(str(source))

    return lx.fromstring(source)
