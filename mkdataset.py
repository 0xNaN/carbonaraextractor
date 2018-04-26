import os
import lxml.html as lx
import nltk

def count_parents(start, stop):
    parents = 0
    while start is not stop:
        start = start.getparent()
        parents += 1
    return parents

def depth(item):
    leaves = item.xpath(".//*[not(*)]")
    max_depth = 0
    for l in leaves:
        max_depth = max(max_depth, count_parents(l, item))

    return max_depth

def relevants_words(item, wordlist):
    porter = nltk.stem.PorterStemmer()
    number_relevants = 0
    for w in item.text_content().split(" "):
        s = porter.stem(w.strip())
        if s in wordlist:
            number_relevants += 1
    return number_relevants

def csv_line(item, features, other=[]):
    f = []
    for k, v in sorted(other, key=lambda pair: pair[0]):
        f.append(v)

    for name in sorted(features.keys()):
        feature_value = features[name](item)
        f.append(str(feature_value))

    return "\t".join(f)

def csv_header_from_features(features, other=[]):
    header = []
    for k in sorted(other):
        header.append(k)

    header = header + sorted(features.keys())
    return "\t".join(header)




#dataset_path = os.sep.join(["..", "camera"])
dataset_path = "/run/media/nan/agiw/camera/"

table_features = {
    "number_tr":     lambda item:  len(item.xpath(".//tr")),
    "number_th":     lambda item:  len(item.xpath(".//th")),
    "number_td":     lambda item:  len(item.xpath(".//td")),
    "number_links":  lambda item:  len(item.xpath(".//a[@href]")),
    "depth": depth,
    "number_relevants": lambda item: relevants_words(item, CAMERA_HOT_WORDS)
}
ground_xpath_file = "table.txt"

domain2xpath = {}
with open(ground_xpath_file, "r") as gf:
    for line in gf.readlines():
        domain = line.split("\t")[0]
        xpath = line.split("\t")[1]

        if domain not in domain2xpath:
            domain2xpath[domain] = []

        domain2xpath[domain].append(xpath.strip())


print(csv_header_from_features(table_features, other=['file', 'relevant']))

for domain in domain2xpath:
#for domain in ["amazon.com"]:
    if domain == "amazon.com":
        continue
    if domain == "walmart.com":
        continue

    for page in os.listdir(os.sep.join([dataset_path, domain])):
        if not page.endswith("html"):
            continue


        file_name = os.sep.join([domain, page])
        full_file_path = os.sep.join([dataset_path, file_name])
        dom = lx.parse(full_file_path)

        relevants_items = set()

        # apply any known xpath and save features of any item
        for xpath in domain2xpath[domain]:
            items = dom.xpath(xpath)
            for item in items:
                relevants_items.add(item)

                print(csv_line(item, table_features, other=[('file', file_name),
                                                            ('relevant', "1")]))

        # save features of any other table
        for item in dom.xpath("//table"):
            if item not in relevants_items:
                print(csv_line(item, table_features, other=[('file', file_name),
                                                            ('relevant', "0")]))
