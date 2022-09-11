from math import log
import operator

def calcShannonEnt(dataset):  # Calculate the entropy of a dataset based on the label value (the last column)
    valueCounts = {}
    for sample in dataset:
        currentLabel = sample[-1] # 5th value of each sample
        if currentLabel not in valueCounts.keys(): # checks how many unique 5th values are there, and how many times each one existed
            valueCounts[currentLabel] = 0
        valueCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in valueCounts:
        prob = float(valueCounts[key]) / len(dataset) 
        shannonEnt -= prob * log(prob, 2)
    return shannonEnt

# takes all the samples whose value i is equal to "value", removes value i from all of them, and return them in a list
def splitDataSet(dataset, i, value):
    retDataSet = []
    for sample in dataset:
        if sample[i] == value:
            reducedFeatVec = featVec[:i]     #chop out axis used for splitting
            reducedFeatVec.extend( featVec[i+1:] )   # The extend() method adds all the elements of an iterable (list, tuple, string etc.) to the end of the list.
            retDataSet.append(reducedFeatVec)
    return retDataSet

def chooseBestFeatureToSplit(dataSet):
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0;
    bestFeature = -1
    for i in range(len(dataSet[0]) - 1): # final value of each sample is the label
        featList = [example[i] for example in dataSet] # create a list of 24 where each value is the ith feature of the ith dataset
        uniqueVals = set(featList) # check how many unique values are in the list above and put them in a new list
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy
        if (infoGain > bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature

def majorityCnt(classList):
    classCount={}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

def createTree(dataSet, labels): # dataSet = 24 samples, each sample is a list of 5 values, labels = age, prescipt, astigmatic, tearRate
    classList = [ example[-1] for example in dataSet ] # takes the 5th and final value of every sample 
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

