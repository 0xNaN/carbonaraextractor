import os
import numpy as np

from carbonaraextractor.DomUtils import *

data_path = os.sep.join(__file__.split("/")[:-2] + ["data"])
with open(os.sep.join([data_path, "and", "camera_hot_words.txt"]), "r") as cf:
    CAMERA_HOT_WORDS = list(map(str.strip, cf.readlines()))
    CAMERA_HOT_WORDS = set(CAMERA_HOT_WORDS)

table_selected = [
    'depth',
    'number_bold',
    'number_br',
    'number_div',
    'number_img',
    'number_li',
    'number_links',
    'number_p',
    'number_relevants',
    'number_td',
    'number_th',
    'number_tr',
    'relevants_ratio'
]

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

list_selected = [
    'avg_tag_in_li',
    'depth',
    'number_bold',
    'number_br',
    'number_div',
    'number_img',
    'number_links',
    'number_p',
    'number_relevants',
    'number_row',
    'relevants_ratio'
]

def avg_tag_in_li(node):
    tags = [len(li.xpath(".//*")) for li in node.xpath(".//li")]
    if len(tags) == 0:
        return 0
    return np.mean(tags)

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
