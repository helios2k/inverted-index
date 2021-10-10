from preprocess import *
from nltk.tokenize import word_tokenize
import json
from tqdm import tqdm

myfile = "./cacm/cacm.all"
output = open("output", "w")
prep = Preprocess([
    Punctuation(),
    Consecutive(),
    Lower(),
    RemoveEmoji(),
    Digits(),
])
stemmer = Stemmer()

'''
    Extract all titles and abstracts in cacm.all and store to dictionaries:
    doc_id {
    "title" : "" , 
    "abstract" : ""
    } 
'''
def getTitlesAbstracts(stem):
    with open (myfile, "r") as infile:
        data = infile.read()
        lines = data.splitlines()
        total_lines = len(lines)
        result = {}
        for i, line in enumerate(lines):
            if line.startswith(".I"):
                doc_id = line.split(' ')[-1]
                result[doc_id] = {}
            # Check if line starts with .T, loop through the next field to get title content
            elif line.startswith(".T"):
                titles = []
                for nextline in lines[i+1:]:
                    if nextline.startswith("."):
                        titles = " ".join(titles)
                        break
                    titles.append(nextline)
                titles = prep(titles)[0]
                if stem:
                    result[doc_id]["title"] = stemmer(titles)
                else:
                    result[doc_id]["title"] = titles
            # Check if line starts with .W, loop through the next field to get abstract content
            elif line.startswith(".W"):
                titles = []
                for nextline in lines[i+1:]:
                    if nextline.startswith("."):
                        titles = " ".join(titles)
                        break
                    titles.append(nextline)
                titles = prep(titles)[0]
                if stem:
                    result[doc_id]["abstract"] = stemmer(titles)
                else:
                    result[doc_id]["abstract"] = titles
                # all_terms = stopwordRemove(all_terms)
    # Save output to data.json because data type is hashmap
    if stem:
        filename = "data_stem.json"
    else:
        filename = "data.json"
    with open(filename, "w") as outfile:
        json.dump(result, outfile)

def readjson(stem):
    if stem:
        filename = "data_stem.json"
    else: 
        filename = "data.json"
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
        return data
# Get all the values of titles and abstracts which are all the terms, from output file
# Store as a list
def getAllTerms(data):
    result = set()
    for key,value in data.items():
        title = value['title']
        if("abstract" in value.keys()):
            abstract = value['abstract']
        else:
            abstract = ""        
        all_terms = " ".join([title,abstract])
        all_terms = word_tokenize(all_terms)
        all_terms = prep(all_terms)
        result.update(all_terms)
    result = list(result)
    return result
'''
doc_id {
    "term" : doc_frequency  
    } 
'''
def countDF(all_term,data):
    result = {}
    for term in tqdm(all_term):
        result[term] = 0
        for key,value in data.items():
            title = value['title']
            if("abstract" in value.keys()):
                abstract = value['abstract']
            else:
                abstract = ""        
            document = " ".join([title,abstract])
            if(term in document):
                result[term] += 1
    return result
'''
{ term: 
  { doc_id:  
      {   "freq": tf, 
          "positions": [positions]  
      } 
  }
}
'''
def postings(all_terms, data):
    result = {}
    for key,value in tqdm(data.items()):
        title = value['title'] 
        if("abstract" in value.keys()):
            abstract = value['abstract']
        else:
            abstract = ""
        document = " ".join([title,abstract])
        tokens = word_tokenize(document)
        for w_index,word in enumerate(tokens):
            if(word in all_terms):
                if not word in result.keys():
                    result[word] = {}
                if not key in result[word].keys():
                    result[word][key] = {
                        "term_freq" : 0,
                        "position" : []
                    }
                result[word][key]["term_freq"] += (1.0 / len(tokens))
                result[word][key]["position"].append(w_index+1)
    return result

def invert(stem):
    getTitlesAbstracts(stem)
    data = readjson(stem)
    all_terms = getAllTerms(data)
    all_terms.sort()
    df = countDF(all_terms,data)
    if stem:
        filename = "dictionary_stem.txt"
        filename2 = "posting_stem.txt"
    else:
        filename = "dictionary.txt" 
        filename2 = "posting.txt"
    with open(filename, 'w') as json_file:
        json.dump(df,json_file)
    post = postings(all_terms, data)
    with open(filename2, 'w') as json_file:
        json.dump(post,json_file)
    
