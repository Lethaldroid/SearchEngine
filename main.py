import json
import glob
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from collections import defaultdict
stop_words = set(stopwords.words("english"))
snow_stemmer = SnowballStemmer(language='english')

filenames = []
lex_dictionary = {}
fi_dictionary = defaultdict(list)
fp_lex = open("lexicon.txt", "w")
fp_fi = open("forwardindex.txt", "w")

docid = -1
key = 0
# making of lexicon
for fname in glob.glob("newsdata/*.json"):
    fp = open(fname, "r")
    y = json.load(fp)

    for i in range(len(y)):
        docid = docid + 1
        word_tokens = word_tokenize(y[i]["content"])
        word_tokens = [w.lower() for w in word_tokens]
        table = str.maketrans('', '', string.punctuation)
        strip = [w.translate(table) for w in word_tokens]

        for w in strip:
            if w.isalpha():
                if w not in stop_words:
                    x = snow_stemmer.stem(w)
                    if x not in lex_dictionary:
                        lex_dictionary[x] = key
                        key += 1
                    if x in lex_dictionary:     #making of forward index
                        fi_dictionary[docid].append(lex_dictionary[x])
    print(fp.name)
    print(docid)
json.dump(lex_dictionary, fp_lex)
json.dump(fi_dictionary, fp_fi)
fp_lex.close()
fp_fi.close()