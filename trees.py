'''
Created on Oct 12, 2010
Decision Tree Source Code for Machine Learning in Action Ch. 3
@author: Peter Harrington
'''
from math import log
import operator

def createDataSet(): # 5 samples, 2 features, 1 categorical label
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'yes'],
               [0, 1, 'no']]
    labels = ['no surfacing', 'flippers']
    #change to discrete values
    return dataSet, labels

def calcShannonEnt(dataSet):  # Calculate the entropy of a dataset based on the label value (the last column)
    # length = 24
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        # checks how many unique 3rd values are there, and how many times each one existed
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0

    for key in labelCounts:
        prob = float(labelCounts[key]) / numEntries
        shannonEnt -= prob * log(prob, 2) #log base 2

    return shannonEnt

def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]     #chop out axis used for splitting
            reducedFeatVec.extend( featVec[axis+1:] )   # The extend() method adds all the elements of an iterable (list, tuple, string etc.) to the end of the list.
            retDataSet.append(reducedFeatVec)
    return retDataSet

def chooseBestFeatureToSplit(dataSet):
    # each sample is a list of 5, so numFeatures = 4
    numFeatures = len(dataSet[0]) - 1
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0;
    bestFeature = -1

    for i in range(numFeatures):        #iterate over all the features
        # create a list of 24 where each value is the ith feature of the ith dataset
        featList = [example[i] for example in dataSet]
        # check how many unique values are in the list above and put them in a new list
        uniqueVals = set(featList)
        newEntropy = 0.0

        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy     #calculate the info gain; ie reduction in entropy

        if (infoGain > bestInfoGain):       #compare this to the best gain so far
            bestInfoGain = infoGain         #if better than current best, set to best
            bestFeature = i

    return bestFeature                      #returns an integer

def majorityCnt(classList):
    classCount={}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]  # if the terminating block contains multiple samples, what's the major class?
    # decision tree can be used for both classification and regression
    # a terminating block can contain multiple samples for generalization
    # classification, voting and find the majority class
    # regression, calculate the mean

# dataSet = 24 samples, each sample is a list of 5 values
# labels = age, prescipt, astigmatic, tearRate
def createTree(dataSet, labels): # feature names in the dataset
    
    # takes the 5th and final value of every sample 
    classList = [ example[-1] for example in dataSet ]

    if classList.count( classList[0] ) == len(classList): # all label values are the same in the dataset, for example: all "yes" or all "no"
        return classList[0] # stop splitting when all of the classes are equal

    if len( dataSet[0] ) == 1: # only 1 column now which is the label value, stop splitting when there are no more features in dataSet
        return majorityCnt(classList) # if the terminating block contains multiple samples, what's the major class?

    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = { bestFeatLabel : {} }
    del( labels[bestFeat] )

    featValues = [ example[bestFeat] for example in dataSet ]  # all the sample values for the selected feature name
    uniqueVals = set(featValues)  # how many unique values for the selected feature name

    for value in uniqueVals:
        subLabels = labels[:]       #copy all of labels, so trees don't mess up existing labels
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)

    return myTree

def classify(inputTree, featLabels, testVec):
    firstStr = list(inputTree)[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    key = testVec[featIndex]
    valueOfFeat = secondDict[key]
    # in prediction, recursion also must be used
    # classify will keep recuring until it reaches a leaf, then enter the else and find the leaf, which is the classLabel
    if isinstance(valueOfFeat, dict):
        classLabel = classify(valueOfFeat, featLabels, testVec)
    else:
        classLabel = valueOfFeat
    return classLabel

def storeTree(inputTree, filename):
    import pickle
    fw = open(filename, 'wb')
    pickle.dump(inputTree, fw)
    fw.close()

def grabTree(filename):
    import pickle
    fr = open(filename, 'rb')
    return pickle.load(fr)

