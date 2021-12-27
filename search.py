import collections
import functools
import itertools
import json
import string
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
fp_ti = open("titleinverted.json", "r")
titleIndex = json.load(fp_ti)
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
        if str(wordid) in invertedIndex:
            elem = invertedIndex[f"{wordid}"]
            sth = OrderedDict(sorted(elem.items(), key=lambda item: len(item[1]), reverse=True))
            return sth
        else:
            return []
    else:
        return []


def singlewordwithid(wordid):
    if wordid in lexicon.values():
        elem = invertedIndex[str(wordid)]
        sth = OrderedDict(sorted(elem.items(), key=lambda item: len(item[1]), reverse=True))
        return sth
    else:
        return []


def titleCheck(word):
    stemmedWord = snow_stemmer.stem(word)
    if stemmedWord in lexicon:
        wordid = lexicon[stemmedWord]
        if str(wordid) in titleIndex:
            titlesearch = titleIndex[f"{wordid}"]
            return titlesearch


search = ""
while search != "-1":
    search = input("Enter your search : ")
    wordsInSearch = search.split()
    if len(wordsInSearch) > 1:
        # multiWord(wordsInSearch)
        wordslist = []
        result = {}
        temp = defaultdict(list)
        mwq = {}
        proximity = {}
        intitle = []
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
                    result[lexicon[x]] = singleword(x)

        for w in wordslist:
            if str(w) in titleIndex:
                title = titleIndex[str(w)]
                intitle.extend(title)

        if len(wordslist) > 1:
            common_set = functools.reduce(set.intersection, (set(val) for val in result.values()))
            common_title = [item for item, count in collections.Counter(intitle).items() if count > 1]
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

            i = 0
            for docid in common_set:
                for i in range(len(mwq[docid]) - 1):
                    mwq[docid][0] = intersection(mwq[docid][0], mwq[docid][i + 1])
                    if len(mwq[docid][0]) != 0:
                        proximity[docid] = mwq[docid][0]

            print("The intitle is: ", common_title)
            if len(intitle) > 0:
                print("\n------------TITLE OCCURRENCES-----------------\n")
                for t in common_title:
                    if t is None:
                        continue
                    else:#printing urls from docs where the words from query occur i.e common set
                        print(url_dic[f"{t}"])

            print("\n------------OTHER OCCURRENCES-----------------\n")
            if len(common_set) == 0:
                print("No such combination of words exist in the database")
                for wordids in wordslist:# if there is no word from query in title or in close proximity or common in some document
                    sth = singlewordwithid(wordids)
                    if len(sth) > 0:
                        for key in sth.keys():
                            print(url_dic[f"{key}"])
                            break
                    else:
                        continue
            else:# printing words in close proximity first and the ones in common set later
                if len(proximity) != 0:
                    for val in proximity.keys():
                        print(url_dic[f"{val}"])
                    for value in common_set:
                        if value not in proximity.keys():
                            print(url_dic[f"{value}"])

        elif len(wordslist) == 1: # if there is only 1 word from the multiword query that is in lexicon
            for wordids in wordslist:
                sth = singlewordwithid(wordids)
                if len(sth) > 0:
                    for key in sth.keys():
                        print(url_dic[f"{key}"])

        else: # if there is no word from the multiword query that is in lexicon
            print("No such combinations of words or individial words exist in the dataset")

    else:
        ts = titleCheck(search)
        if ts is None:
            ts = []
        sws = singleword(search)

        if len(ts) > 0 or len(sws) > 0:
            if len(ts) > 0:
                print("\n------------TITLE OCCURRENCES-----------------\n")
                for t in ts:
                    print(url_dic[f"{t}"])
            if len(sws) > 0:
                print("\n------------OTHER OCCURRENCES-----------------\n")
                for key in sws.keys():
                    print(url_dic[f"{key}"])
        else:
            print("No such word exists in the database")