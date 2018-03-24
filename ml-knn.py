# -*- coding: utf-8 -*-
"""
Created on Thu Sep 18 12:25:09 2014

@author: mario
"""

import csv
import random
import math
import operator

# Split the data into training and test data
def loadDataset(filename, split, trainingSet=[] , testSet=[]):
    with open(filename, 'rb') as csvfile:
        lines = csv.reader(csvfile)
        dataset = list(lines)
        for x in range(len(dataset)):
            for y in range(4):
                dataset[x][y] = float(dataset[x][y])
            if split == 0 or random.random() < split:
                trainingSet.append(dataset[x])
            else:
                testSet.append(dataset[x])
                
def euclideanDistance(instance1, instance2, length):
    distance = 0
    for x in range(length):
        distance += pow((instance1[x] - instance2[x]), 2)
    return math.sqrt(distance)
    
def getNeighbors(trainingSet, testInstance, k):
    distances = []
    length = len(testInstance)-1
    for x in range(len(trainingSet)):
        dist = euclideanDistance(testInstance, trainingSet[x], length)
        distances.append((trainingSet[x], dist))
    distances.sort(key = operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])
    return neighbors
    
def getResponse(neighbors):
    # Creating a list with all the possible neighbors
    classVotes = {}
    for x in range(len(neighbors)):
        response = neighbors[x][-1]
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1
    sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedVotes[0][0]
    
def getAccuracy(testSet, predictions):
    correct = 0
    for x in range(len(testSet)):
        if testSet[x][-1] == predictions[x]:
            correct += 1
    return (correct/float(len(testSet))) * 100.0
                
def main():
    trainingSet=[]
    trainingSet1=[]
    testSet=[]
    custom_test=[]

    split = 0.67
    loadDataset('accelerometer/1.csv', split, trainingSet, testSet)
    loadDataset('accelerometer/2.csv', split, trainingSet, testSet)
    loadDataset('accelerometer/3.csv', split, trainingSet, testSet)
    loadDataset('accelerometer/4.csv', split, trainingSet, testSet)
    split = 0.9994
    loadDataset('accelerometer/5.csv', split, trainingSet1, custom_test)
    print 'Train set: ' + repr(len(trainingSet))
    print 'Test set: ' + repr(len(testSet))
    print 'Test custom: ' + repr(len(custom_test))
    predictions=[]
    k = 3
    i = 0

    # for x in range(len(testSet)):
    #     neighbors = getNeighbors(trainingSet, testSet[x], k)
    #     result = getResponse(neighbors)
    #     predictions.append(result)
    #
    #     i += 1
    #     print(repr(i) + '> predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1]))
    # accuracy = getAccuracy(testSet, predictions)
    # print 'Accuracy: ', accuracy

    print('Custom test!')
    predictions = []
    for x in range(len(custom_test)):
        neighbors = getNeighbors(trainingSet, custom_test[x], k)
        result = getResponse(neighbors)
        predictions.append(result)

        i+=1
        print(repr(+i) + '> predicted=' + repr(result) + ', actual=' + repr(custom_test[x][-1]))
    accuracy = getAccuracy(custom_test, predictions)
    print 'Custom Accuracy: ', accuracy

main()