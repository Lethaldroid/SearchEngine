import json
import glob
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

filtered_sentence = []
dictionary = {}

stop_words = set(stopwords.words("english"))
snow_stemmer = SnowballStemmer(language='english')
fp_lex = open("lexicon.txt", "w")
docid = -1
key = 0

# t0 = time.time()

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
                    filtered_sentence.append(x)
                    if x not in dictionary:
                        dictionary[x] = key
                        key += 1
    print(fp.name)
    print(docid)
json.dump(dictionary, fp_lex)
fp_lex.close()
# t1 = time.time()
# total = t1-t0
# print(total)
