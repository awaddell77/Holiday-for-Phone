from C_sort import *
def dictionarify(x):
    #should produce list of dictionaries from a csv, with the column headers as the keys
    item = C_sort(x)
    items = item.contents
    crit = item.contents[0]
    results = []
    for i in range(1, len(items)):
        d = dict.fromkeys(crit, 0)
        for i_2 in range(0, len(items[i])):
            d[crit[i_2]] = items[i][i_2]
        results.append(d)
    return results