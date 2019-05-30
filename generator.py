''' We parse each document of each file from our data set '''
''' This results in a dictionary docID:content '''


def docsToDict(fname):

    docs = {}
    backup = {}
    with open(fname) as in_file:
        lines = [[line.rstrip('\n')] for line in in_file]
    
    position = 0
    for line in lines:
        # print(line)
        if '<doc id=' in line[0]:
            elements = line[0].split()
            docID = elements[1][4:-1]
            url = elements[2][5:-1]
            title = elements[3][7:]

            docs[docID] = []
            backup[docID] = [title, url]
        elif '</doc>' in line[0]:
            docID = None
        else:
            if docID and line[0] != '':
                docs[docID].extend(line) 

docsToDict('wiki_01')