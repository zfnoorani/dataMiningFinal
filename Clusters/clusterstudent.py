# Zamin Noorani
# HW 2
# This HW will do agglomerate clustering with datasets that have multiple attributes. Will use single or complete linkage.
'''
Agglomerative Clustering
'''

from __future__ import division
from collections import defaultdict


# find the normalized distance
def nDistance(item1, item2, nvalue):
    return abs(item1 - item2)
    # return (abs(item1 - item2))/nvalue


def singleLinkage(clusterDist, newClusterName, originalDist, clusterNames):
    # add to clusterDist new distances from new cluster to all other clusters
    # use closest distances between clusters
    for s1 in clusterNames:
        smallestD = 9999
        cnList = s1.split(' ')
        for cElem in cnList:
            # handle newClusterName changed to comma delimited string
            ncList = newClusterName.split(' ')
            for ncElem in ncList:
                if float(originalDist[cElem][ncElem]) < float(smallestD):
                    smallestD = originalDist[cElem][ncElem]
        clusterDist[newClusterName][s1] = smallestD
        clusterDist[s1][newClusterName] = smallestD



def completeLinkage(clusterDist, newClusterName, originalDist, clusterNames):
    # very similar to single linkage - copied and pasted singleLinkage method skelaton -
    # add to clusterDist new distances from new cluster to all other clusters
    # use farthest distances between clusters
    for s1 in clusterNames:
        largestD = 0
        cnList = s1.split(' ')
        for cElem in cnList:
            # handle newClusterName changed to comma delimited string
            ncList = newClusterName.split(' ')
            for ncElem in ncList:
                if float(originalDist[cElem][ncElem]) > float(largestD):
                    largestD = originalDist[cElem][ncElem]
        clusterDist[newClusterName][s1] = largestD
        clusterDist[s1][newClusterName] = largestD


def normalize(needToNormalize, finalNorm, min, max):
    # This function is used to normalize a column of tuple data. We have an array of the column of data we need to normalize called needToNormalize
    # We also have a finalNorm array which is an array that we will add the normalized data to. The min and max are the min and max within the column of data.
    maxMinusMin = max - min
    length = len(needToNormalize)
    itemsVal = float(0)
    # print("needToNormalize ---> ", needToNormalize, "MIN ----> ", min, "Max----> ", max)
    for i in range(length):
        if (maxMinusMin == 0):
            # If a certain corresponding attribute of all the tuples is the same than the distance is 0, since we dont want to divide by 0 we do the following
            finalNorm[i] = finalNorm[i] + itemsVal
        else:
            itemsVal = (needToNormalize[i] - min) / maxMinusMin
            # Normalized value is: (value - min value in column)/(max value in column - min value in column)
            finalNorm[i] = finalNorm[i] + itemsVal
            # finalNorm is added to.


def main():
    userInput = int(input("Type 0 or 1\n0 - Single Linkage\n1 - Complete linkage\n"))
    # Want user to choose linkage type

    # Initialization and Read in Sequences
    originalDist = defaultdict(lambda: defaultdict(int))
    clusterDist = defaultdict(lambda: defaultdict(int))

    infile = open('clusterdata.txt', 'r')
    itemNames = []
    items = []
    # read in item names
    line = infile.readline().rstrip('\n')

    # print(line)
    # print(len(line))
    itemNames = line.split(' ')
    # print("item name",itemNames)
    # get item data
    line = infile.readline().rstrip('\n')
    numCol = len(line.split(" "))
    # Set line equal the second row so we can get length of number of columns.
    min = 9999
    max = 0
    infile.seek(0)
    infile.readline()
    # restart infile read to first row
    if (numCol == 1):
        # if only one data attribute no need to normalize.
        for line in infile:
            line = float(line.replace('\n', ''))
            # code should support floats hence above float
            items.append(line)
            # slight flaw in logic for min/max
            if line < min:
                min = line
            elif line > max:
                max = line
        print(min, max, (max - min))
        print(itemNames, '\n')
        print(items, '\n')
    else:
        needToNormalize = []
        # get item data
        for i in range(len(itemNames)):
            items.append(0)
            # items in this case is normalized items. Set normalized item values to 0 as we will be adding to them later.
        for i in range(numCol):
            min = 9999
            max = 0
            for l in infile:
                columnValues = float(l.split()[i])
                # Going through the column of a tuple attribute so we can ge the normalized value
                # print(i, " ---> This is the i :", columnValues, "----> this is the col:")
                needToNormalize.append(columnValues)
                if columnValues < min:
                    min = columnValues
                elif columnValues > max:
                    max = columnValues
                # Need the min and max for normalization
            normalize(needToNormalize, items, min, max)
            # Normalize column values, items will be the where we want to add these values to.
            infile.seek(0)
            infile.readline()
            # restart infile read to first row
            needToNormalize = []
            # empty array so we can add the next column of data to it.

    # Step 1: Create distance matrix
    for iItem, iName in zip(items, itemNames):
        for jItem, jName in zip(items, itemNames):
            if iName == jName:
                d = 0
            else:
                d = nDistance(iItem, jItem, (max - min))
            originalDist[iName][jName] = d
            clusterDist[iName][jName] = d
    # print(originalDist)
    # print(clusterDist)

    clusterNames = itemNames
    loopctr = 1

    # Step 2: Perform Agglomerative Clustering
    numClust=input("How many clusters do you want [Max: 166 Min: 1]\n")
    numClust = ((int)(numClust))
    while len(clusterNames) > numClust:
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
        newClusterName = shortestI + ' ' + shortestJ
        clusterNames.remove(shortestI)
        clusterNames.remove(shortestJ)

        del clusterDist[shortestI]
        del clusterDist[shortestJ]

        klist = list(clusterDist.keys())
        for k in klist:
            k2list = list(clusterDist[k])
            for k2 in k2list:
                if (k2 == shortestI or k2 == shortestJ):
                    del clusterDist[k][k2]
                # add new cluster and distances to matrix
        if (userInput != 1):
            # choosing linkage method
            singleLinkage(clusterDist, newClusterName, originalDist, clusterNames)
        else:
            completeLinkage(clusterDist, newClusterName, originalDist, clusterNames)
        clusterNames.append(newClusterName)
        print('_____________________________________________________iteration__________________________________________________________', loopctr)
        #print(clusterNames)
        for i in clusterNames:
            print(i,'\n')
        loopctr += 1


        #print(clusterDist)
        # user=input("Do you want to interate?")
        # if(user=='0'):
        #     loopctr += 1
        #     print("____________________________", len(clusterNames))
        #     continue
        # elif(user==1):
        #     break




main()
