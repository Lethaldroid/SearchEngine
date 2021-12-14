import json
import glob
import pickle
import time
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from collections import defaultdict
import os.path

write = 0
start_time = time.time()
stop_words = set(stopwords.words("english"))
snow_stemmer = SnowballStemmer(language='english')
fp_filenames = open('filecount.txt', "a+")

if os.path.isfile("lexicon.json"):
    fp_lex = open("lexicon.json", "r")
    lex_dictionary = json.load(fp_lex)
    fp_lex.close()
    fp_lex = open("lexicon.json", "w")

    fp_fi = open("forwardindex.pkl", "rb")
    fi_dictionary= pickle.load(fp_fi)
    fp_fi.close()
    fp_fi = open("forwardindex.pkl", "wb")

    fp_ii = open("invertedindex.pkl", "rb")
    ii_dictionary = pickle.load(fp_ii)
    fp_ii.close()
    fp_ii = open("invertedindex.pkl", "wb")
else:
    fp_lex = open("lexicon.json", "w")
    fp_fi = open("forwardindex.pkl", "wb")
    fp_ii = open("invertedindex.pkl", "wb")
    lex_dictionary = {}
    fi_dictionary = defaultdict(list)
    ii_dictionary = defaultdict(list)
fp_temp = open("storage.txt", "r")
key = int(fp_temp.readline())
docid = int(fp_temp.readline())
fp_temp.close()


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


# making of lexicon
for fname in glob.glob("newsdata/*.json"):
    fp = open(fname, "r")

    if fp_filenames.mode == 'a+':
        if not check_if_string_in_file('filecount.txt',fname.lower()):
            print("opening if new file added in dataset")
            fp_filenames.write(fp.name)
            fp_filenames.write("\n")
            y = json.load(fp)
            for i in range(len(y)):
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
                            if x in lex_dictionary:  # making of forward index
                                if lex_dictionary[x] not in fi_dictionary[docid]:
                                    fi_dictionary[docid].append(lex_dictionary[x])
                                ii_dictionary[lex_dictionary[x]].append(docid)
                docid = docid + 1
            print(fp.name)
            print(docid)
            write = 1
        else:
            print("went to next file")
            continue

fp_temp = open("storage.txt", "w")
fp_temp.write(str(key))
fp_temp.write("\n")
fp_temp.write(str(docid))
if write == 1:
    json.dump(lex_dictionary, fp_lex)
    pickle.dump(fi_dictionary, fp_fi)
    pickle.dump(ii_dictionary, fp_ii)
    fp_fit = open("forwardindex.json","w")
    json.dump(fi_dictionary, fp_fit)
    fp_fit.close()
    fp_iit = open("invertedindex.json", "w")
    json.dump(ii_dictionary, fp_iit)
    fp_iit.close()

fp_ii.close()
fp_lex.close()
fp_fi.close()

fp_filenames.close()
fp_temp.close()
print(time.time() - start_time)
