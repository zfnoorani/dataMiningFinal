from __future__ import division
from collections import defaultdict
import math

class Node :
    __parent = None
    __branchvalues = []
    __children = []
    __value = None
    __count = 0


    def __init__(self, p=None, b=[],  c=[], v=None, ct=0):
        print('in constructor for node ' + v)
        print(self)
        print("parent ", end='')
        print(p, end='')
        print(' value ', v, end='')
        print(' count ', ct)

        self.__parent = p
        self.__branchvalues = b
        self.__children = c
        self.__value = v
        self.__count = ct

    def getParent(self): return self.__parent
    def getValue(self): return self.__value
    def getCount(self): return self.__count

    def incrCount(self): self.__count+=1

    def findChild(self, val):
        # search for val in children nodes
        # return None if not found, else return found Node
        i = 0
        found = None
        while (i<self.numChildren() and found == None):
            if(self.getChild(i).getValue() == val):
                found = self.getChild(i)
            i+=1
        return found

    def addChild(self, val):
        childNode = Node(self, [], val, 1)
        self.__children.append(childNode)
        return childNode

    def numChildren(self):
        return len(self.__children)

    def getChild(self, idx):
        if (idx >= 0 and idx < len(self.__children)):
            return self.__children[idx]
        else:
            return None

    def getBranchValue(self, idx):
        if (idx >= 0 and idx < len(self.__branchvalues)):
            return self.__branchvalues[idx]
        else:
            return None

    def printNode(self):
        print('Parent ', end='')
        if(self.__parent == None):
            print('None', end='')
        else:
            print(self.__parent.__value, end='')
        print(' Value ', self.__value, end='')
        print(' Count ', self.__count)

def calcEntropy(tuples, slot):
    # calculate counts for each value of attribute in position slot
    values = {}
    numTuples = len(tuples)
    numAttrs = len(tuples[0])
    counts = [0, 0, 0] # total count for value, pos count, neg count
    for i in range(numTuples):
        v = tuples[i][slot]
        if (values.get(v) != None):
            counts = values[v]
            if (tuples[i][numAttrs-1] == 'y'):
                counts[0] += 1
            else:
                counts[1] += 1
            values[v] = counts
        else:
            if (tuples[i][numAttrs-1] == 'y'):
                values[v] = [1, 0]
            else:
                values[v] = [0, 1]

    entropy = 0
    for v in values:
        counts = values[v]
        totalCounts = counts[0] + counts[1]
        pos = counts[0]/totalCounts
        if (pos != 0):
            pos = -(pos * math.log2(pos))
        neg = counts[1]/totalCounts
        if (neg != 0):
            neg = -(neg * math.log2(neg))
        entropy += ((totalCounts/numTuples) * (pos + neg))

    return entropy

def getIPN(tuples):
    numTuples= len(tuples)
    print(tuples)
    print(" Num Tuples ", numTuples)
    pos = 0
    for i in range(numTuples):
        #if there are 5 attribute values and a total of 6 tuples than subtract 2
        print(tuples[i][numTuples-1])
        if (tuples[i][numTuples-1] == 'y'):
            pos+=1
    neg = numTuples-pos
    print("neg: ", neg)

    pos = pos/numTuples
    neg = neg/numTuples
    return (-pos * math.log2(pos)) - (neg * math.log2(neg))

def main():
    try:
        infile = open('classdata.txt', 'r')
    except (OSError, IOError):
        print("error - file not found")
        exit(-1)

    attrs = []
    tuples = []

    # first line is attribute names
    dataLine = infile.readline().rstrip('\n')

    if (dataLine):
        attrs = dataLine.split(',')
    else:
        print("no data in file")
        exit(-1)

    # start processing tuple data
    dataLine = infile.readline().rstrip('\n')
    while(dataLine != ''):
        dataLine = dataLine.split(',')
        tuples.append(dataLine)
        dataLine = infile.readline().rstrip('\n')

    ipn = round(getIPN(tuples),2)
    print(ipn, "IPN")
    gains = []
    for i in range(len(attrs)-1):
        e = round(calcEntropy(tuples, i),2)
        gains.append(round(ipn-e, 2))

    print(attrs)
    print(tuples)
    print(ipn)
    print(gains)

main()
