''' This file handles the query part of the search engine '''

import numpy
from numpy import zeros



def filesToDicts():
    
    ind = {}
    mapp = {}
    pos = {}

    mat = numpy.loadtxt('vectorSpace.txt')
    with open('index.txt') as ind_file, open("mapping.txt", 'r') as mapp_file, open("positions.txt", "r") as pos_file:
        ind_lines = [[line.rstrip('\n')] for line in ind_file]
        ind_lines = [line[0] for line in ind_lines]
        mapp_lines = [[line.rstrip('\n')] for line in mapp_file]
        mapp_lines = [line[0].split(' ') for line in mapp_lines]
        pos_lines = [[line.rstrip('\n')] for line in pos_file]
        pos_lines = [line[0].split(' ') for line in pos_lines]
    
    for line in ind_lines:
        split = line.split(' ')
        word, postings = split[0], [i for i in split[1:]]
        ind[word] = postings

    for line in mapp_lines:
        mapp[line[0]] = line[1]
    
    for line in pos_lines:
        pos[line[0]] = line[1]
    
    return mat, ind, mapp, pos



matrix, index, mapping, position = filesToDicts()


