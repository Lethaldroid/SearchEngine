import json
import glob
import pickle
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from collections import defaultdict
import os.path

stop_words = set(stopwords.words("english"))
snow_stemmer = SnowballStemmer(language='english')
filename = {}
lex_dictionary = {}
fi_dictionary = defaultdict(list)
ii_dictionary = defaultdict(list)
fp_fi = open("forwardindex.txt", "w")
fp_ii = open("invertedindex.txt", "w")
docid = -1
key = 0
file_exists = os.path.exists('filecount.txt')

if file_exists:
    fp_filenames = open('filecount.txt', "a+")
    readfile = fp_filenames.read()
    fp_lex = open("lexicon.txt", "a+")
else:
    fp_filenames = open('filecount.txt', "w")
    fp_lex = open("lexicon.txt", "w")

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
                            if x in lex_dictionary:  # making of forward index
                                fi_dictionary[docid].append(lex_dictionary[x])
            print(fp.name)
            print(docid)
        else:
            print("went to next file")
            continue

    if fp_filenames.mode == 'w':
        print("opening file in write mode")
        fp_filenames.write(fp.name)
        fp_filenames.write("\n")
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
                        if x in lex_dictionary:  # making of forward index
                            fi_dictionary[docid].append(lex_dictionary[x])
                            ii_dictionary[lex_dictionary[x]].append(docid)
        print(fp.name)
        print(docid)
json.dump(lex_dictionary, fp_lex)
json.dump(fi_dictionary, fp_fi)
json.dump(ii_dictionary,fp_ii)
fp_ii.close()
fp_lex.close()
fp_fi.close()
fp_filenames.close()
