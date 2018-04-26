import nltk
import lxml.html as lx

def count_xpath(node, xpath):
    return len(node.xpath(xpath))

def count_stem(node, stems, sep=" "):
    porter = nltk.stem.PorterStemmer()
    num_found = 0

    #TODO: maybe we have to delete symbols
    for word in node.text_content().split(sep):
        word = word.strip()
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
