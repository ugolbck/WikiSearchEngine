def manyIntersect(index, query):
    # Sorting by length of postings list
    query.sort(key = lambda l: len(index[l]))
    
    result = index[quey[0]]
    del query[0]
    
    while query and result:
        # comp, result = skipIntersect(index, result, term_list[0])
        result = skipIntersect(index, result, query[0])
        del query[0]

    # Return the final intersection 
    return result


def skipIntersect(index, post1, term2):
    # We sort the lists when using lower_index.txt
    post1.sort()
    post2 = index[term2]
    post2.sort()
    result = []
    # Initialize the skip lists
    skip_1 = skipList(post1)
    skip_2 = skipList(post2)
    i, j = 0, 0
    # starting of the algorithm 
    while i < len(post1) and j < len(post2):
        if post1[i] == post2[j]:
            result.append(post1[i])
            i += 1
            j += 1
        elif post1[i] < post2[j]:
            if skip_1 and skip_1[0] <= post2[j]:
                while skip_1 and skip_1[0] <= post2[j]:
                    i = post1.index(skip_1[0])
                    del skip_1[0]
            else:
                i += 1
        else:
            if skip_2 and skip_2[0] <= post1[i]:
                while skip_2 and skip_2[0] <= post1[i]:
                    j = post2.index(skip_2[0])
                    del skip_2[0]
            else:
                j += 1
    return result

def skipList(post):
    gap = round(math.sqrt(len(post)))
    # Returns the skip list composed of evenly separated numbers from the postings list
    return [post[i] for i in range(1, len(post), gap)]
