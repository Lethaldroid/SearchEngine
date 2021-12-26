import functools
import json
import glob
import sys
import time
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from collections import defaultdict
from collections import OrderedDict

import os.path
fp_lex = open("lexicon.json", "r")
lexicon = json.load(fp_lex)
fp_url = open("urls.json", "r")
url_dic = json.load(fp_url)
fp_inverted = open("invertedindex.json", "r")
invertedIndex = json.load(fp_inverted)
fp_ti = open("titleinverted.json")
titleIndex = json.load(fp_ti)
stop_words = set(stopwords.words("english"))
snow_stemmer = SnowballStemmer(language='english')

def flatten(lst):
    for elem in lst:
        if type(elem) in (tuple, list):
            for i in flatten(elem):
                yield i
        else:
            yield elem


def intersection(lst1, lst2):
    temp = set(lst2)
    lst3 = [value for value in lst1 if value in temp]
    return lst3

def singleword(word):
    stemmedWord = snow_stemmer.stem(word)
    if stemmedWord in lexicon:
        wordId = lexicon[stemmedWord]
        elem = invertedIndex[str(wordId)]
        sth = (OrderedDict(sorted(elem.items(), key=lambda item: len(item[1]), reverse=True)))
        # print(sth)
        return sth


def multi_dict(k, type):
    if k == 1:
        return defaultdict(type)
    else:
        return defaultdict(lambda: multi_dict(k - 1, type))

def titleCheck(word):
    stemmedWord = snow_stemmer.stem(word)
    if stemmedWord in lexicon:
        wordid = lexicon[stemmedWord]
        if wordid in titleIndex.keys():
            title = titleIndex[f"{wordid}"]
            return title
        else:
            return []


def check_if_string_in_file(file_name, string_to_search):
    """ Check if any line in the file contains given string """
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            if string_to_search in line:
                return True
    return False


write = 0
start_time = time.time()
search = ""
while search != "-1":
    search = input("Enter your search : ")
    start = time.time()
    wordsInSearch = search.split()
    if len(wordsInSearch) > 1:
        # multiWord(wordsInSearch)
        listoflists = []
        wordslist = []
        docslist = {}
        res = {}
        commonset = {}
        i=0
        search_tokens = word_tokenize(search)
        search_tokens = [w.lower() for w in search_tokens]
        table = str.maketrans('', '', string.punctuation)
        search_strip = [w.translate(table) for w in search_tokens]
        for w in search_strip:
            if w.isalpha() and w not in stop_words:

                x = snow_stemmer.stem(w)
                if x in lexicon:
                    wordslist.append(lexicon[x])
                    res[lexicon[x]] = singleword(x)
                    # print(set)
                #     wordslist.append(lexicon[x])
                #     docslist[wordslist[i]] = invertedIndex[f"{wordslist[i]}"]
                #     # print(docslist)
                #     print(common_set)
                i = i+1

        commonset = functools.reduce(set.intersection, (set(val) for val in res.values()))

        # sorted(commonset.values())
        print(commonset)
        print(wordslist)
        print("The length: ", len(commonset))
        #wordslist.clear()
        if len(commonset) == 0:
            print("No such combination of words exist in the database")
        else:
            for val in commonset:
                print(url_dic[f"{val}"])

    else:
        tt = titleCheck(search)
        sth = singleword(search)
        if len(tt) > 0 and len(sth) > 0:
            for t in tt:
                print(url_dic[f"{t}"])
            for key in sth.keys():
                print(url_dic[f"{key}"])
        if len(tt) == 0 and len(sth) > 0:
            for key in sth.keys():
                print(url_dic[f"{key}"])
        else:
            print("No such word exists in the database")
    print(time.time()-start)
