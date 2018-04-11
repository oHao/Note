import numpy as np
import os as os
import kNN as knn


# 读取文件，转化成数字数组
def img2vector(fileName):
    returnVector = np.zeros((1, 1024))
    fr = open(fileName)
    for i in range(32):
        line = fr.readline()
        for j in range(32):
            returnVector[0, 32 * i + j] = int(line[j])
    return returnVector


# 测试过程
def handWritingTest():
    # 定义标签
    labels = []
    # 读取文件目录
    fileList = os.listdir('trainingDigits')
    size = len(fileList)
    hwMat = np.zeros((size, 1024))
    for i in range(size):
        # 处理标签
        fileName = fileList[i]
        labels.append(fileName.split('_')[0])
        hwMat[i, :] = img2vector('trainingDigits/%s' % fileName)
    testFileList = os.listdir('testDigits')
    m = len(testFileList)
    errorCount = 0.0
    for i in range(m):
        fileName = testFileList[i]
        label = fileName.split('_')[0]
        inputData = img2vector('testDigits/%s' % fileName)
        result = knn.kNN(inputData, hwMat, labels, 3)
        if label is result:
            print("its Ok")
        else:
            errorCount += 1
            print("keep Going")
    print(errorCount / m)


handWritingTest()
