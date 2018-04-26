from DomUtils import *

with open("data/camera_hot_words.txt", "r") as cf:
    CAMERA_HOT_WORDS = list(map(str.strip, cf.readlines()))

table = {
    "number_tr":        lambda node: count_xpath(node, ".//tr"),
    "number_th":        lambda node: count_xpath(node, ".//th"),
    "number_td":        lambda node: count_xpath(node, ".//td"),
    "number_links":     lambda node: count_xpath(node, ".//a[@href]"),
    "depth":            lambda node: depth(node),
    "number_relevants": lambda node: count_stem(node, CAMERA_HOT_WORDS)
}
