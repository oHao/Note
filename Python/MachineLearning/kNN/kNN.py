from numpy import *
import operator
import matplotlib
import matplotlib.pyplot as plt


'''准备简单数据'''


def createDataSet():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    label = ['A', 'A', 'B', 'B']
    return group, label


''' kNN算法'''


def kNN(inX, dataSet, label, k):
    dataSetSize = dataSet.shape[0]
    diffmat = tile(inX, (dataSetSize, 1)) - dataSet
    sqdiffmat = diffmat**2
    sqdistance = sqdiffmat.sum(axis=1)
    distance = sqdistance**0.5
    sortedDistIndices = distance.argsort()
    classCount = {}
    for i in range(k):
        voteIlabel = label[sortedDistIndices[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


'''读取约会数据'''


def DatingSetMatrix(fileName):
    fr = open(fileName)
    lines = fr.readlines()
    lenth = len(lines)
    matrix = zeros((lenth, 3))
    classLabels = []
    index = 0
    for line in lines:
        line = line.strip()
        datasInLine = line.split('\t')
        matrix[index, :] = datasInLine[0:3]
        classLabels.append(int(datasInLine[-1]))
        index += 1
    return matrix, classLabels


'''归一化特征值'''


def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normSet = dataSet - tile(minVals, (m, 1))
    normSet = normSet / tile(ranges, (m, 1))
    tile
    return normSet, ranges, minVals


''' 测试代码'''


def datingClassTest():
    horatio = 0.05
    group, labels = DatingSetMatrix('datingTestSet2.txt')
    normMat, ranges, minVals = autoNorm(group)
    m = normMat.shape[0]
    numTestVecs = int(m * horatio)
    errorCount = 0
    for i in range(numTestVecs):
        result = kNN(normMat[i, :], normMat[numTestVecs:m, :], labels[numTestVecs:m], 4)
        print("The Result is %d and The Answer is %d" % (result, labels[i]))
        if result != labels[i]:
            errorCount += 1
    print("the error rate is %f" % (errorCount / numTestVecs))

datingClassTest()


