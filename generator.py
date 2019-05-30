''' We parse each document of each file from our data set '''
''' This results in text files with ID name and text content '''

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk
import re

# Turns xml parsed file into separate documents
def docsToFiles(fname, language):

    backup = {}
    folder_path = './DOCUMENTS/'
    with open(fname) as in_file:
        lines = [[line.rstrip('\n')] for line in in_file]

    for line in lines:
        if '<doc id=' in line[0]:
            elements = line[0].split()
            docID = elements[1][4:-1]
            url = elements[2][5:-1]
            title = elements[3][7:]
            flt = []
            backup[docID] = [title, url]
        elif '</doc>' in line[0]:
            with open(folder_path + docID + '.txt', 'w') as f:
                f.write(str(flt)[1:-1])
            docID = None
        else:
            if docID and line[0] != '':
                sl = []
                sl.extend(line)
                s = re.sub(r'[^\w\s]', '', sl[0])
                tokens = nltk.word_tokenize(s.lower())
                new = [w for w in tokens if not w in stopwords.words(language)]
                stemmer = PorterStemmer()
                final = [stemmer.stem(word) for word in new]
                flt.extend(final)
                
    return backup


def vector_index(backup):
    vector_dic = {}
    Ndic = {}
    folder_path = './DOCUMENTS/'
    for k in backup.keys():
        docID = k
        with open(folder_path + docID + '.txt', 'r') as f:
            line = f.read().split(', ')
        Ndic[docID] = len(line)
        for token in line:
            if token not in vector_dic.keys():
                vector_dic[token] = {docID: 1}
            else:
                if docID in vector_dic[token].keys():
                    vector_dic[token][docID] += 1
                else:
                    vector_dic[token][docID] = 1
               
    return Ndic, vector_dic
        

if __name__ == '__main__':
    backup = docsToFiles('wiki_en', 'english')
    lenghts, dico = vector_index(backup)

    print(dico)
    
    
