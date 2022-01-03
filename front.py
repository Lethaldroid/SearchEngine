'''
DSA PROJECT MADE BY:
1. SAIF ALI (336561)
2. HASEEB MAHMOOD (334718)
3. TALHA MAJEED KHAN (336254)
4. ALI USMAN BUTT (335520)

PRESENTED TO: SIR FAISAL SHAFAIT
'''

# Importing external dependencies.
import collections
import functools
import itertools
import json
import os
import string
import tkinter as tk
import webbrowser
from collections import OrderedDict, defaultdict
from tkinter import *
from tkinter import filedialog
from tkinter import font

from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize

# Global variable declarations and loading indexes in to the memory.
fp_temp = open("storage.txt", "r")
key = int(fp_temp.readline())
docid = int(fp_temp.readline())
fp_temp.close()

fp_a = open("author.json", "r")
author_dictionary = json.load(fp_a)
fp_a.close()

fp_filenames = open('filecount.txt', "a+")

fp_lex = open("lexicon.json", "r")
lex_dictionary = json.load(fp_lex)
fp_lex.close()

fp_url = open("urls.json", "r")
url_dic = json.load(fp_url)
fp_url.close()

fp_inverted = open("invertedindex.json", "r")
ii_dictionary = json.load(fp_inverted)
fp_inverted.close()

fp_ti = open("titleinverted.json", "r")
titleIndex = json.load(fp_ti)
fp_ti.close()

stop_words = set(stopwords.words("english"))
snow_stemmer = SnowballStemmer(language='english')
write = 0


# Class to create vertical scrollable frame to show urls to the user.
class VerticalScrolledFrame(tk.Frame):
    """A pure Tkinter scrollable frame that actually works!

    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """

    def __init__(self, parent, *args, **kw):
        tk.Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                           yscrollcommand=vscrollbar.set)
        # canvas.place(x=2,y=200)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = tk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=tk.NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())

        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())

        canvas.bind('<Configure>', _configure_canvas)


# Destroy the current result frame and create a new frame.
def clear():
    scframe.destroy()
    create()


# Get query from the user. (The text written in search bar)
def getquery():
    clear()
    lis.clear()
    e = user_query.get()
    searching(str(e), lis)
    for i, x in enumerate(lis):
        btn = tk.Button(scframe.interior, height=1, width=74, relief=tk.FLAT, bg="gray99", fg="blue", font="Dosis",
                        text=f"{lis[i]}", command=lambda i=i, x=x: openlink(i))
        btn.pack(padx=10, pady=5, side=tk.TOP)


# Create a scrollable frame to show to the user.
def create():
    global scframe
    scframe = VerticalScrolledFrame(root)
    scframe.pack(side='bottom', pady=30)


# Make the urls that are received as strings and convert them to hyperlinks.
def openlink(i):
    webbrowser.open_new(lis[i])


# Take the intersection of common lists.
def intersection(lst1, lst2):
    temp = set(lst2)
    lst3 = [value for value in lst1 if value in temp]

    if (len(lst3)) == 0:
        return []
    else:
        return lst3


def diff(a, val):
    a = [x - val for x in a]
    return a


# searching a single word and returning result as a list by passing a word.
def singleword(word):
    stemmedword = snow_stemmer.stem(word)
    if stemmedword in lex_dictionary:
        wordid = lex_dictionary[stemmedword]
        if str(wordid) in ii_dictionary:
            elem = ii_dictionary[f"{wordid}"]
            sth = OrderedDict(sorted(elem.items(), key=lambda item: len(item[1]), reverse=True))
            return sth
        else:
            return []
    else:
        return []


# searching in authors and returning result as a list by passing a word
def authorsearch(word):

    sth = [value for key, value in author_dictionary.items() if word in key.lower()]
    if len(sth) > 0:
        sth = list(flatten(sth))
        return sth
    else:
        return []


# searching a single word and returning result as a list by passing a wordid.
def singlewordwithid(wordid):
    if str(wordid) in ii_dictionary:
        elem = ii_dictionary[str(wordid)]
        sth = OrderedDict(sorted(elem.items(), key=lambda item: len(item[1]), reverse=True))
        return sth
    else:
        return []


# Checking the search in title.
def titleCheck(word):
    stemmedWord = snow_stemmer.stem(word)
    if stemmedWord in lex_dictionary:
        wordid = lex_dictionary[stemmedWord]
        if str(wordid) in titleIndex:
            titlesearch = titleIndex[f"{wordid}"]
            return titlesearch


def searching(search, lis):
    '''
    The searching functions perform the searching.
    **** FOR SINGLE WORD SEARCH ****
    -> Title occurrences are shown first.
    -> Occurrence in content are then shown.

    *** FOR MULTIWORD SEARCH ***
    -> Title with all or more than 1 words in it are shown.
    -> Content with all words coming together as a string is shown.
    -> Content with all the words regardless of their positions are shown.
    -> Single word occurrences in title are shown.
    -> Single word in contents are displayed at last.

    *** NON EXISTING WORD ***
    -> No result is shown.
    -> Console displays that word does not exist.
    '''
    searchquery = search
    wordsInSearch = searchquery.split()

    # multi-words\author searching.
    if ".author" in wordsInSearch:
        x = searchquery.split(".author ")
        auth_name = "".join(x)
        x = auth_name.split()
        auth_name = "".join(x)
        auth_name = auth_name.lower()
        res = authorsearch(auth_name)
        if len(res) > 0:
            counter = 0
            for values in res:
                lis.append(url_dic[f"{values}"])
                counter += 1
                if counter == 60:
                    break
        else:
            print("\nno such author exists\n")

    elif len(wordsInSearch) > 1:
        wordslist = []
        result = {}
        temp = defaultdict(list)
        mwq = {}
        proximity = {}
        intitle = []
        rp = defaultdict(list)
        search_tokens = word_tokenize(searchquery)  # Tokenizes the query.
        search_tokens = [w.lower() for w in search_tokens]
        table = str.maketrans('', '', string.punctuation)  # Removes the punctuations.
        search_strip = [w.translate(table) for w in search_tokens]

        for w in search_strip:
            if w.isalpha() and w not in stop_words:
                x = snow_stemmer.stem(w)
                if x in lex_dictionary:
                    wordslist.append(lex_dictionary[x])
                    result[lex_dictionary[x]] = singleword(x)

        for w in wordslist:
            if str(w) in titleIndex:
                title = titleIndex[str(w)]
                intitle.extend(title)

        if len(wordslist) > 1:
            common_set = functools.reduce(set.intersection, (set(val) for val in result.values()))
            common_title = [item for item, count in collections.Counter(intitle).items() if count > 1]
            i = 0
            for value in common_set: #applying relative postioning algortithm on docids of common set
                for wid in wordslist:
                    rp[i].append(ii_dictionary[f"{wid}"][f"{value}"])
                i += 1
            i = 0
            for val, docid in itertools.zip_longest(range(len(rp)), common_set):
                for value in rp[val]:
                    temp[docid].append(diff(value, i))
                    i += 1
                mwq[docid] = temp[docid]
                i = 0

            i = 0
            for docid in common_set: #separting docids where close proximity occurences are found
                for i in range(len(mwq[docid]) - 1):
                    mwq[docid][0] = intersection(mwq[docid][0], mwq[docid][i + 1])
                    if len(mwq[docid][0]) != 0:
                        proximity[docid] = mwq[docid][0]
            if len(common_title) > 0:
                print("\n------------TITLE OCCURRENCES-----------------\n")
                count = 0
                for t in common_title:
                    if t is None:
                        continue
                    else:  # printing urls from docs where the words from query occur i.e common set
                        lis.append(url_dic[f"{t}"])
                        count +=1
                        if count == 30:
                            break

            if len(common_set) == 0:
                print("No such combination of words exist in the database")
                for wordids in wordslist:  # if there is no word from query in title or in close proximity or common in some document
                    sth = singlewordwithid(wordids)
                    counter = 0
                    if len(sth) > 0:
                        for key in sth.keys():
                            lis.append(url_dic[f"{key}"])
                            counter += 1
                            if counter == 30:
                                break
                    else:
                        continue
            else:  # printing words in close proximity first and the ones in common set later
                if len(proximity) != 0:
                    print("\n------------CLOSE PROXIMITY OCCURRENCES-----------------\n")
                    var = 0
                    for val in proximity.keys():
                        lis.append(url_dic[f"{val}"])
                        var +=1
                        if var == 30:
                            break
                    print("\n------------OTHER OCCURRENCES---------------------------\n")
                    var = 0
                    for value in common_set:
                        if value not in proximity.keys():
                            lis.append(url_dic[f"{value}"])
                            var+=1
                            if var == 30:
                                break
                else:
                    print("\n------------OTHER OCCURRENCES---------------------------\n")
                    var = 0
                    for value in common_set:
                        if value not in proximity.keys():
                            lis.append(url_dic[f"{value}"])
                            var += 1
                            if var == 30:
                                break
        elif len(wordslist) == 1:  # if there is only 1 word from the multiword query that is in lex_dictionary
            for wordids in wordslist:
                sth = singlewordwithid(wordids)
                counter = 0
                if len(sth) > 0:
                    for key in sth.keys():
                        lis.append(url_dic[f"{key}"])
                        counter += 1
                        if counter == 30:
                            break

        else:  # if there is no word from the multiword query that is in lex_dictionary
            print("No such combinations of words or individial words exist in the dataset")

    else:
        ts = titleCheck(searchquery)
        if ts is None:
            ts = []
        sws = singleword(searchquery)
        counter = 0
        if len(ts) > 0 or len(sws) > 0:
            if len(ts) > 0:
                print("\n------------TITLE OCCURRENCES-----------------\n")
                for t in ts:
                    lis.append(url_dic[f"{t}"])
                    counter += 1
                    if counter == 30:
                        break
            if len(sws) > 0:
                print("\n------------OTHER OCCURRENCES-----------------\n")
                counter = 0
                for key in sws.keys():
                    lis.append(url_dic[f"{key}"])
                    counter += 1
                    if counter == 30:
                        break
        else:
            print("No such word exists in the database")


# Flatten functions is used to remove extra brackets in dictionary if they may occur.
def flatten(lst):
    for elem in lst:
        if type(elem) in (tuple, list):
            for i in flatten(elem):
                yield i
        else:
            yield elem


# For creation of multi-dictionary.
def multi_dict(k, type):
    if k == 1:
        return defaultdict(type)
    else:
        return defaultdict(lambda: multi_dict(k - 1, type))


# This function is used to check if the file already exists in dataset or not.
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


# Get file from the user to add it into data set.
def getFile():
    filepath = str()
    file = filedialog.askopenfile(mode='r')
    if file:
        filepath = os.path.abspath(file.name)
        updateall(filepath, key, docid, fp_filenames)


# Updating the dataset, inverted index and lexicon. (May take up to 1 min)
def updateall(filetoadd, key, docid, fp_filenames):
    fp = open(filetoadd, 'r')
    if not check_if_string_in_file('filecount.txt', os.path.basename(fp.name)):
        print("new file added in dataset")
        print(os.path.basename(fp.name))
        fp_filenames.write(os.path.basename(fp.name))
        fp_filenames.write("\n")
        y = json.load(fp)
        for i in range(len(y)):
            position = 0
            word_tokens = word_tokenize(y[i]["content"])
            url_dic[f"{docid}"] = y[i]["url"]               #updating urls
            author_tokens = word_tokenize(y[i]["author"])   #updating authors
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
                        # making of lex_dictionary
                        lex_dictionary[x] = key
                        key += 1
                    if x in lex_dictionary:  # making of inverted index
                        if str(lex_dictionary[x]) not in ii_dictionary:
                            # wordid does not exist
                            ii_dictionary.update({f"{lex_dictionary[x]}": {}})
                        if str(lex_dictionary[x]) in ii_dictionary:
                            if str(docid) not in ii_dictionary[f"{lex_dictionary[x]}"]:
                                # wordid exists but doc id doesnt
                                ii_dictionary[f"{lex_dictionary[x]}"][f"{docid}"] = [position]
                            elif str(docid) in ii_dictionary[f"{lex_dictionary[x]}"]:
                                # wordid and docid exists
                                temp_list = [ii_dictionary[f"{lex_dictionary[x]}"][f"{docid}"]]
                                temp_list = list(flatten(temp_list))
                                temp_list.append(position)
                                ii_dictionary[f"{lex_dictionary[x]}"][f"{docid}"] = temp_list
                    position += 1
            for t in title_strip:#updating title
                if t.isalpha() and t not in stop_words:
                    t = snow_stemmer.stem(t)
                    if t not in lex_dictionary:
                        lex_dictionary[t] = key
                        key += 1
                    if t in lex_dictionary:
                        if str(lex_dictionary[t]) not in titleIndex:
                            titleIndex[f"{lex_dictionary[t]}"] = [docid]
                        if str(lex_dictionary[t]) in titleIndex:
                            if docid not in titleIndex[f"{lex_dictionary[t]}"]:
                                titleIndex[f"{lex_dictionary[t]}"].append(docid)
            docid = docid + 1
        fp_temp = open("storage.txt", "w")
        fp_temp.write(str(key))
        fp_temp.write("\n")
        fp_temp.write(str(docid))
        fp_temp.close()
        fp_ii = open("invertedindex.json", "w")
        fp_lex = open("lexicon.json", "w")
        fp_url = open("urls.json", "w")
        fp_ti = open("titleinverted.json", "w")
        fp_a = open("author.json", "w")
        json.dump(author_dictionary, fp_a)
        json.dump(lex_dictionary, fp_lex)
        json.dump(ii_dictionary, fp_ii)
        json.dump(url_dic, fp_url)
        json.dump(titleIndex, fp_ti)
        fp_url.close()
        fp_ii.close()
        fp_lex.close()
        fp_ti.close()
        fp_a.close()
        fp_filenames.close()
    print("updation successfull")


print("Initializing GUI")

root = tk.Tk()
root.title("Search Engine")
root.geometry('800x500')
root['bg'] = '#FFFFFF'
root.minsize(800, 500)
root.maxsize(800, 500)
lis = []
user_query = tk.StringVar()
logo_path = tk.PhotoImage(file="BG.ppm")
logo = Label(root, image=logo_path).pack()
button_font = font.Font(family='Arial', size=8)
text_entry = tk.Entry(root, textvariable=user_query, width=55, bg='#C0C0C0').place(x=230, y=120)
search_button = tk.Button(root, text="search", font=button_font, padx=1, pady=1, command=getquery).place(x=375, y=150)
add_file_button = tk.Button(root, text="add file", font=button_font, padx=4, pady=2, command=getFile).place(x=740, y=10)
scframe = VerticalScrolledFrame(root)
scframe.pack(side='bottom', pady=30)

root.mainloop()
