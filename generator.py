''' We parse each document of each file from our data set '''
''' This results in a dictionary docID:content '''

from nltk.corpus import stopwords
import nltk
import re

# Turns xml parsed file into dictionary of document contents
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
                f.write(str(flt))
            docID = None
        else:
            if docID and line[0] != '':
                sl = []
                sl.extend(line)
                s = re.sub(r'[^\w\s]', '', sl[0])
                tokens = nltk.word_tokenize(s.lower())
                # print(tokens)
                new = [w for w in tokens if not w in stopwords.words(language)]
                flt.extend(new)
                
    return backup

        

if __name__ == '__main__':
    backup = docsToFiles('wiki_01', 'french')
    
