''' This file handles the query part of the search engine '''

import numpy
from numpy import zeros
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk
import re


def filesToDicts():

    ind = {}
    mapp = {}
    pos = {}
    
    with open('index.txt', 'r') as ind_file, open("mapping.txt", 'r') as mapp_file, open("positions.txt", "r") as pos_file:
        ind_lines = [[line.rstrip('\n')] for line in ind_file]
        ind_lines = [line[0] for line in ind_lines]
        mapp_lines = [[line.rstrip('\n')] for line in mapp_file]
        mapp_lines = [line[0].split(' ') for line in mapp_lines]
        pos_lines = [[line.rstrip('\n')] for line in pos_file]
        pos_lines = [line[0].split(' ') for line in pos_lines]
    
    # Matrix
    mat = numpy.loadtxt('vectorSpace.txt')

    # Index
    for line in ind_lines:
        split = line.split(' ')
        word, postings = split[0], [i for i in split[1:]]
        ind[word] = postings

    # Mapping
    for line in mapp_lines:
        mapp[line[0]] = line[1]
    
    # Positions
    for line in pos_lines:
        pos[line[0]] = line[1]
    
    return mat, ind, mapp, pos

# Query sanitizer (stopwords, lowercase, stemming, tokenizing)
def query_sanity(query, language):

    stemmer = PorterStemmer()
    query = re.sub(r'[^\w\s]', '', str(query))
    tokens = nltk.word_tokenize(query.lower())
    if len(tokens) >= 1:
        filtered = [w for w in tokens if not w in stopwords.words(language)]
        sane_query= [stemmer.stem(word) for word in filtered]
    else:
        sane_query = []
    
    return sane_query

# Query vector generator
def query_vector(query, pos, ind):
  if query == []:
    return "the query search you were looking for is a stop word, which is not supported by our search engine"
  else:
    vect = zeros(len(ind.keys()))
    for word in query:
        if pos.get(word):
            vect[int(pos[word])] = 1
  return vect


matrix, index, mapping, positions = filesToDicts()

dummy = 'history invisible greek'
sane_dummy = query_sanity(dummy, 'english')
vector = query_vector(sane_dummy, positions, index)

print(vector)


