'''
Agglomerative Clustering
'''

from __future__ import division
from collections import defaultdict

# find the normalized distance
def nDistance(item1, item2, nvalue):
    return abs(item1-item2)
    #return (abs(item1 - item2))/nvalue

def singleLinkage(clusterDist, newClusterName, originalDist, clusterNames):
    # add to clusterDist new distances from new cluster to all other clusters
    # use closest distances between clusters
    for s1 in clusterNames:
        smallestD = 9999
        cnList = s1.split(' ')
        for cElem in cnList:
            # handle newClusterName changed to comma delimited string
            ncList = newClusterName.split(' ');
            for ncElem in ncList:
                if float(originalDist[cElem][ncElem]) < float(smallestD):
                    smallestD = originalDist[cElem][ncElem]
        clusterDist[newClusterName][s1] = smallestD
        clusterDist[s1][newClusterName] = smallestD

def main():
    # Initialization and Read in Sequences
    originalDist = defaultdict(lambda:defaultdict(int))
    clusterDist = defaultdict(lambda:defaultdict(int))


    infile = open('clusterdata.txt', 'r')
    itemNames = []
    items = []
    # read in item names
    line = infile.readline().rstrip('\n')
    itemNames = line.split(' ')
    # get item data
    min = 9999
    max = 0
    for line in infile:
        line = int(line.replace('\n', ''))

        items.append(line)
        # slight flaw in logic for min/max
        if line < min:
            min = line
        elif line > max:
            max = line
    print(min, max, (max-min))
    print(itemNames)
    print(items)

    # Step 1: Create distance matrix
    for iItem, iName in zip(items, itemNames):
        for jItem, jName in zip(items, itemNames):
            if iName == jName:
                d = 0
            else:
                d = nDistance(iItem, jItem, (max-min))
            originalDist[iName][jName] = d
            clusterDist[iName][jName] = d
    print(originalDist)
    print(clusterDist)

    clusterNames = itemNames
    loopctr = 1

    # Step 2: Perform Agglomerative Clustering
    while len(clusterNames) > 1:
        # find shortest distance in clusterDist
        shortestD = clusterDist[clusterNames[0]][clusterNames[1]]
        shortestI = clusterNames[0]
        shortestJ = clusterNames[1]
        for iName in clusterNames:
            for jName in clusterNames:
                if (iName != jName and float(clusterDist[iName][jName]) < float(shortestD)):
                    shortestD = clusterDist[iName][jName]
                    shortestI = iName
                    shortestJ = jName

        # merge clusters i and j
        #newClusterName = shortestI + shortestJ
        newClusterName = shortestI + ' ' + shortestJ
        clusterNames.remove(shortestI)
        clusterNames.remove(shortestJ)

        del clusterDist[shortestI]
        del clusterDist[shortestJ]

        klist = list(clusterDist.keys())
        print("****", klist)
        for k in klist:
            k2list = list(clusterDist[k])
            for k2 in k2list:
                if (k2 == shortestI or k2 == shortestJ):
                    del clusterDist[k][k2]

                # add new cluster and distances to matrix
        print("single linkage", newClusterName)
        singleLinkage(clusterDist, newClusterName, originalDist, clusterNames)
        clusterNames.append(newClusterName)
        print('iteration', loopctr)
        print(clusterNames)
        print(clusterDist)
        loopctr+=1

main()