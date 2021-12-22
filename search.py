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
