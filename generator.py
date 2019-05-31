''' We parse each document of each file from our data set '''
''' This results in text files with ID name and text content '''

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk
import re
from numpy import zeros
import numpy as np
import math

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
                flt = re.sub(r'[^\w\s]', '', str(flt))
                f.write(flt)
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


def indexing(backup):
    index_dic = {}
    Ndic = {}
    posDic = {}
    position = 0
    folder_path = './DOCUMENTS/'
    
    for k in backup.keys():
        docID = k
        with open(folder_path + docID + '.txt', 'r') as f:
            line = f.read().split(' ')
        Ndic[docID] = len(line)
        for token in line:
            if token not in index_dic.keys():
                index_dic[token] = {docID: 1}
                posDic[token] = position
                position += 1
            else:
                if docID in index_dic[token].keys():
                    index_dic[token][docID] += 1
                else:
                    index_dic[token][docID] = 1
    
    return Ndic, index_dic, posDic


# Creation of a vector space (matrix) containing all documents vectors
def doc_vector(ind, back, pos, docLen):
    mapping = {}
    matrix = zeros(shape=(len(back.keys()), len(ind.keys())))
    pointer = 0
    for i in back.keys():
        file_words = set()
        for k, v in ind.items():
            if i in v.keys():
                file_words.add(k)
        for j in file_words:
            tf = ind[j][i] / docLen[i]
            idf = math.log(len(back.keys())/(len(ind[j])))
            matrix[pointer][pos[j]] = tf * idf
            mapping[i] = pointer
        pointer += 1
    with open('vectorSpace.txt', 'w') as vec, open('mapping.txt', 'w') as mapp:
            np.savetxt(vec, matrix, fmt='%.6f')
            for key, val in mapping.items():
                docID, row = str(key), str(val)
                mapp.write(docID + ' ' + row + '\n')
    
        
    
        

        

if __name__ == '__main__':
    backup = docsToFiles('wiki_en', 'english')
    docLenghts, index, positions = indexing(backup)
    doc_vector(index, backup, positions, docLenghts)


    # print(backup)
    
    
