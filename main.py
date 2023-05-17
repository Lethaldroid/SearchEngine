import json
import glob
import time
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from collections import defaultdict
import os.path


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
stop_words = set(stopwords.words("english"))
snow_stemmer = SnowballStemmer(language='english')
fp_filenames = open('filecount.txt', "a+")

if os.path.isfile("lexicon.json"):
    fp_lex = open("lexicon.json", "r")
    lex_dictionary = json.load(fp_lex)
    fp_lex.close()

    fp_url = open("urls.json", "r")
    url_dictionary = json.load(fp_url)
    fp_url.close()

    fp_ii = open("invertedindex.json", "r")
    ii_dictionary = json.load(fp_ii)
    fp_ii.close()

    fp_fi = open("forwardindex.json", "r")
    fi_dictionary = json.load(fp_fi)
    fp_fi.close()

    fp_ti = open("titleinverted.json", "r")
    title_dictionary = json.load(fp_ti)
    fp_ti.close()

    fp_a = open("author.json", "r")
    author_dictionary = json.load(fp_a)
    fp_a.close()
else:
    url_dictionary = {}
    lex_dictionary = {}
    author_dictionary = defaultdict(list)
    fi_dictionary = defaultdict(list)
    ii_dictionary = multi_dict(2, list)
    title_dictionary = defaultdict(list)
if os.path.isfile("storage.txt"):
    fp_temp = open("storage.txt", "r")
    try:
        key = int(fp_temp.readline())
        docid = int(fp_temp.readline())
    except:
        key = 0
        docid = 0
    fp_temp.close()
else:
    key = 0
    docid = 0

# making of lexicon
for fname in glob.glob("newsdata/*.json"):
    fp = open(fname, "r")

    if fp_filenames.mode == 'a+':
        if not check_if_string_in_file('filecount.txt', os.path.basename(fname.lower())):
            print("new file added in dataset")
            fp_filenames.write(os.path.basename(fname.lower()))
            fp_filenames.write("\n")
            y = json.load(fp)
            for i in range(len(y)):
                position = 0
                word_tokens = word_tokenize(y[i]["content"])
                url_dictionary[f"{docid}"] = y[i]["url"]

                author_tokens = word_tokenize(y[i]["author"])
                author_tokens = [w.lower() for w in author_tokens]
                author = "".join(author_tokens)
                author_dictionary[f'{author}'].append(docid)

                title_tokens = word_tokenize(y[i]["title"])
                
                word_tokens = [w.lower() for w in word_tokens]
                table = str.maketrans('', '', string.punctuation)
                strip = [w.translate(table) for w in word_tokens]
                
                title_tokens = [t.lower() for t in title_tokens]
                title_table = str.maketrans('', '', string.punctuation)
                title_strip = [t.translate(title_table) for t in title_tokens]
                for w in strip:
                    if w.isalpha() and w not in stop_words:
                        x = snow_stemmer.stem(w)
                        if x not in lex_dictionary:
                            # making of lexicon
                            lex_dictionary[x] = key
                            key += 1
                        if x in lex_dictionary:  # making of inverted index
                            if str(lex_dictionary[x]) not in ii_dictionary:
                                ii_dictionary.update({f"{lex_dictionary[x]}": {}})
                                ii_dictionary.update({f"{lex_dictionary[x]}": {}})
                            if str(lex_dictionary[x]) in ii_dictionary:
                                # wordid does not exist
                                if str(docid) not in ii_dictionary[f"{lex_dictionary[x]}"]:
                                    # wordid exists but doc id doesnt
                                    ii_dictionary[f"{lex_dictionary[x]}"][f"{docid}"] = [position]
                                elif str(docid) in ii_dictionary[f"{lex_dictionary[x]}"]:
                                    # wordid and docid exists
                                    temp_list = [ii_dictionary[f"{lex_dictionary[x]}"][f"{docid}"]]
                                    temp_list = list(flatten(temp_list))
                                    temp_list.append(position)
                                    ii_dictionary[f"{lex_dictionary[x]}"][f"{docid}"] = temp_list
                            if str(docid) not in fi_dictionary:
                                # making of forward index                              fi_dictionary[f"{docid}"] = [lex_dictionary[x]]                          if str(docid) in fi_dictionary:
                                if lex_dictionary[x] not in fi_dictionary[f"{docid}"]:
                                    fi_dictionary[f"{docid}"].append(lex_dictionary[x])
                        position += 1
                for t in title_strip:
                    if t.isalpha() and t not in stop_words:
                        t = snow_stemmer.stem(t)
                        if t not in lex_dictionary:
                            lex_dictionary[t] = key
                            key += 1
                        if t in lex_dictionary:
                            if str(lex_dictionary[t]) not in title_dictionary:
                                title_dictionary[f"{lex_dictionary[t]}"] = [docid]
                            if str(lex_dictionary[t]) in title_dictionary:
                                if docid not in title_dictionary[f"{lex_dictionary[t]}"]:
                                    title_dictionary[f"{lex_dictionary[t]}"].append(docid)
                docid = docid + 1
            print(fp.name)
            print(docid)
            write = 1
        else:
            continue

fp_temp = open("storage.txt", "w")
fp_temp.write(str(key))
fp_temp.write("\n")
fp_temp.write(str(docid))
fp_temp.close()
if write == 1:
    fp_fi = open("forwardindex.json", "w")
    fp_ii = open("invertedindex.json", "w")
    fp_lex = open("lexicon.json", "w")
    fp_url = open("urls.json", "w")
    fp_ti = open("titleinverted.json", "w")
    json.dump(lex_dictionary, fp_lex)
    json.dump(fi_dictionary, fp_fi)
    json.dump(ii_dictionary, fp_ii)
    json.dump(url_dictionary, fp_url)
    json.dump(title_dictionary, fp_ti)
    fp_url.close()
    fp_ii.close()
    fp_lex.close()
    fp_ti.close()

try:
    fp_fi.close()
except:
    pass
fp_a = open("author.json", "w")
json.dump(author_dictionary,fp_a)
fp_a.close()
fp_filenames.close()
print(time.time() - start_time)
