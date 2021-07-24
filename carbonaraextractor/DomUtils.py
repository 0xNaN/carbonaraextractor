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

def node_text_summary(node, length=50):
    words = [n.text_content().strip() for n in node.xpath(".//*[not(*)]")]
    text = " ".join(words).strip()
    text = re.sub(r"\s+", " ", text)
    return text[:length]

def clean_node(node):
    # remove any comments, script, ...
    cleaner = lx.clean.Cleaner()
    node = cleaner.clean_html(node)

    for br in node.xpath(".//br"):
        br.tail = "\n" + br.tail if br.tail else "\n"
    lx.etree.strip_elements(node, 'br', with_tail=False)

    return node

## XXX: has side-effect: translate <br> to "\n"
def node_to_key_value(node):
    key = value = None

    node = clean_node(node)
    while (key == None):

        children = node.getchildren()

        # empty
        if len(children) == 0:
            raise Exception("EmptyNode")

        # <tag>key</tag>value
        elif len(children) == 1 and children[0].tail != None and children[0].tail.strip() != "":
            value = children[0].tail
            key = children[0].text_content()

        # key<tag>value</tag>
        elif len(children) == 1 and node.text != None and node.text.strip() != "":
            value = children[0].text_content()
            key = node.text

        # <wraptag>..[...]..</wraptag>
        elif len(children) == 1:
            node = node.getchildren()[0]

        # <tag>key</tag><tag1>the</tag1><tag2>value</tag>
        else:
            key = children[0].text_content()

            children.pop(0)
            value = " ".join(map(lambda n: n.text_content(), children))

    # whitespace chars (\n included) -> " "
    key = re.sub(r'\s+', " ", key).strip()

    # all whitespace chars but \n -> " "
    value = re.sub(r'[^\S\n]+', " ", value).strip()
    value = re.sub(r'\s*\n\s*', "\n", value).strip()

    return (key, value)
