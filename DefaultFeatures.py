import statistics

from DomUtils import *

with open("data/camera_hot_words.txt", "r") as cf:
    CAMERA_HOT_WORDS = list(map(str.strip, cf.readlines()))
    CAMERA_HOT_WORDS = set(CAMERA_HOT_WORDS)

table_selected = ['number_bold',
                  'number_img',
                  'number_links',
                  'number_relevants',
                  'number_td',
                  'relevants_ratio',
                  'number_tr']
table = {
    "number_tr":        lambda node: count_xpath(node, ".//tr"),
    "number_th":        lambda node: count_xpath(node, ".//th"),
    "number_td":        lambda node: count_xpath(node, ".//td"),
    "number_links":     lambda node: count_xpath(node, ".//a[@href]"),
    "depth":            lambda node: depth(node),
    "number_relevants": lambda node: count_stem(node, CAMERA_HOT_WORDS),
    "relevants_ratio": lambda node: count_stem(node, CAMERA_HOT_WORDS) / len(node_stems(node)),
    "number_bold":      lambda node: count_xpath(node, ".//b") +
                                     count_xpath(node,".//strong"),
    "number_p": lambda node: count_xpath(node, ".//p"),
    "number_br": lambda node: count_xpath(node, ".//br"),
    "number_img": lambda node: count_xpath(node, ".//img"),
    "number_li": lambda node: count_xpath(node, ".//li"),
    "number_div": lambda node: count_xpath(node, ".//div"),
}


list_selected = ['number_bold',
                 'number_img',
                 'number_links',
                 'number_relevants',
                 'avg_tag_in_li',
                 'relevants_ratio']

def avg_tag_in_li(node):
    tags = [len(li.xpath(".//*")) for li in node.xpath(".//li")]
    if len(tags) == 0:
        return 0
    return statistics.mean(tags)

list = {
    "number_row": lambda node: count_xpath(node, ".//li") + count_xpath(node, ".//dt"),
    "number_relevants": lambda node: count_stem(node, CAMERA_HOT_WORDS),
    "relevants_ratio": lambda node: count_stem(node, CAMERA_HOT_WORDS) / len(node_stems(node)),
    "number_links":     lambda node: count_xpath(node, ".//a[@href]"),
    "number_bold":      lambda node: count_xpath(node, ".//b") +
                                     count_xpath(node,".//strong"),
    "number_img": lambda node: count_xpath(node, ".//img"),
    "number_div": lambda node: count_xpath(node, ".//div"),
    "number_p": lambda node: count_xpath(node, ".//p"),
    "number_br": lambda node: count_xpath(node, ".//br"),
    "depth":    lambda node: depth(node),
    "avg_tag_in_li": avg_tag_in_li
}
