import functools
import itertools
import json
import time
import string
# import numpy
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from collections import OrderedDict, defaultdict

fp_lex = open("lexicon.json", "r")
lexicon = json.load(fp_lex)
fp_url = open("urls.json", "r")
url_dic = json.load(fp_url)
fp_inverted = open("invertedindex.json", "r")
invertedIndex = json.load(fp_inverted)
stop_words = set(stopwords.words("english"))
snow_stemmer = SnowballStemmer(language='english')


def intersection(lst1, lst2):
    temp = set(lst2)
    lst3 = [value for value in lst1 if value in temp]

    if (len(lst3)) == 0:
        return []
    else:
        return lst3


def Diff(a, val):
    a = [x - val for x in a]
    return a


def singleword(word):
    stemmedword = snow_stemmer.stem(word)
    if stemmedword in lexicon:
        wordid = lexicon[stemmedword]
        elem = invertedIndex[str(wordid)]
        sth = OrderedDict(sorted(elem.items(), key=lambda item: len(item[1]), reverse=True))
        return sth


start_time = time.time()
search = ""
while search != "-1":
    search = input("Enter your search : ")
    start = time.time()
    wordsInSearch = search.split()
    if len(wordsInSearch) > 1:
        # multiWord(wordsInSearch)
        wordslist = []
        res = {}
        temp = defaultdict(list)
        mwq = {}
        dic2 = {}
        rp = defaultdict(list)
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

        common_set = functools.reduce(set.intersection, (set(val) for val in res.values()))
        i = 0
        for value in common_set:
            for wid in wordslist:
                rp[i].append(invertedIndex[f"{wid}"][f"{value}"])
            i += 1

        i = 0
        for val, docid in itertools.zip_longest(range(len(rp)), common_set):
            for value in rp[val]:
                temp[docid].append(Diff(value, i))
                i += 1
            mwq[docid] = temp[docid]
            i = 0
        print(mwq)

        i = 0
        for docid in common_set:
            for i in range(len(mwq[docid]) - 1):
                mwq[docid][0] = intersection(mwq[docid][0], mwq[docid][i + 1])
                if len(mwq[docid][0]) != 0:
                    dic2[docid] = mwq[docid][0]
        print(dic2)
        print(wordslist)
        print(rp)
        print(common_set)

        if len(common_set) == 0:
            print("No such combination of words exist in the database")
        else:
            if len(dic2)!=0:
                for val in dic2.keys():
                    print(url_dic[f"{val}"])
                for value in common_set :
                    if value not in dic2.keys():
                        print(url_dic[f"{value}"])

    else:
        sth = singleword(search)
        if len(sth) > 0:
            for key in sth.keys():
                print(url_dic[f"{key}"])
        else:
            print("No such word exists in the database")
    print(time.time() - start)
