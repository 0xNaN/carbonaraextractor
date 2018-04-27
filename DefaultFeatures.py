from DomUtils import *

with open("data/camera_hot_words.txt", "r") as cf:
    CAMERA_HOT_WORDS = list(map(str.strip, cf.readlines()))

table_selected = ['number_bold',
                  'number_img',
                  'number_links',
                  'number_relevants',
                  'number_td',
                  'number_tr']
table = {
    "number_tr":        lambda node: count_xpath(node, ".//tr"),
    "number_th":        lambda node: count_xpath(node, ".//th"),
    "number_td":        lambda node: count_xpath(node, ".//td"),
    "number_links":     lambda node: count_xpath(node, ".//a[@href]"),
    "depth":            lambda node: depth(node),
    "number_relevants": lambda node: count_stem(node, CAMERA_HOT_WORDS),
    "number_bold":      lambda node: count_xpath(node, ".//b") +
                                     count_xpath(node,".//strong"),
    "number_p": lambda node: count_xpath(node, ".//p"),
    "number_br": lambda node: count_xpath(node, ".//br"),
    "number_img": lambda node: count_xpath(node, ".//img"),
    "number_li": lambda node: count_xpath(node, ".//li"),
    "number_div": lambda node: count_xpath(node, ".//div")
}
