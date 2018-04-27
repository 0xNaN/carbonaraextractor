import nltk
import requests
import re
import lxml.html as lx

def count_xpath(node, xpath):
    return len(node.xpath(xpath))

def count_stem(node, stems, sep=" "):
    porter = nltk.stem.PorterStemmer()
    num_found = 0

    #TODO: maybe we have to delete symbols
    for word in node_words(node):
        stem = porter.stem(word)
        if stem in stems:
            num_found += 1

    return num_found

def depth(node):
    max_depth = 0
    leaves = node.xpath(".//*[not(*)]")

    for leave in leaves:
        max_depth = max(max_depth, count_between(leave, node))

    return max_depth

def count_between(start_node, stop_node):
    parents = 0
    while start_node is not stop_node:
        start_node = start_node.getparent()
        parents += 1
    return parents

def node_words(node):
    text = " ".join(node.itertext())
    text = re.sub(r"[^a-z0-9]", " ", text, flags=re.IGNORECASE)
    return re.split(r'\W+', text)

def domFromUrl(url, dump_on=""):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
    }

    r = requests.get(url, headers=headers)

    if dump_on != "":
        with open(dump_on, "w") as d:
            d.write(r.text)

    return lx.fromstring(r.text)
