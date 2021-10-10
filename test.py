
from stopwords import stopwordRemove
from stemmer import stemmer
from main import readjson
from nltk.tokenize import word_tokenize
import json

def inputProcess(term,stem,stop):
    with open("dictionary.txt") as json_file:
        data = json.load(json_file)
        df = data[term]
    with open("posting.txt") as json_file:
        data = json.load(json_file)
        doc_id = list(data[term].keys())[0]
        postings = data[term]
        position = data[term][doc_id]["position"][0]-1
    data = readjson(stem)
    document = data[doc_id]
    title = document['title']
    if("abstract" in document.keys()):
        abstract = document['abstract']
    else:
        abstract = ""        
    all_terms = " ".join([title,abstract])
    words = word_tokenize(all_terms)
    highlight = f"\033[44;33m{words[position]}\033[m"
    words_precede = " ".join(words[position-5:position])
    words_follow = " ".join(words[position+1:position+6])
    print(" ".join([words_precede,highlight,words_follow]))
    print("----------------------")
    print("Document Frequency: ", df)
    print("Postings list: ", postings)

def test():
    stem = False
    sw = False
    while True:
        inputText = input("Enter term(s): ")
        if inputText.lower() == "zzend":
            break
        elif inputText == "stem":
            stem = True
        elif inputText == "sw":
            sw = True
        try:
            result = inputProcess(inputText,stem=False,stop=False)
        except KeyError:
            print("Term not found")
    
test()