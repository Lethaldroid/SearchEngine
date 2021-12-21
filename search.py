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
fp_inverted = open("invertedindex.json", "r")
invertedIndex = json.load(fp_inverted)
stop_words = set(stopwords.words("english"))
snow_stemmer = SnowballStemmer(language='english')

def flatten(lst):
    for elem in lst:
        if type(elem) in (tuple, list):
            for i in flatten(elem):
                yield i
        else:
            yield elem


def multi_dict(k, type):
    if k == 1:
        return defaultdict(type)
    else:
        return defaultdict(lambda: multi_dict(k - 1, type))


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

search = input("Enter your search : ")
start = time.time()
wordsInSearch = search.split()
if len(wordsInSearch) > 1:
    # multiWord(wordsInSearch)
    print(" ")
else:
    stemmedWord = snow_stemmer.stem(search)
    wordId = lexicon[stemmedWord]
    elem = invertedIndex[str(wordId)]
    sth = OrderedDict(sorted(elem.items(), key=lambda item: len(item[1]), reverse=True))
    for key in sth.keys():
        print(key)
    #print(listoflist)
print(time.time()-start)