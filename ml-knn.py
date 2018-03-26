# -*- coding: utf-8 -*-
"""
Created on Thu Sep 18 12:25:09 2014

@author: mario
"""

import csv
import random
import math
import operator
from matplotlib import pyplot as plt
import numpy as np

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


def getNormalVote(neighbors):
    votes = {}
    for x in range(len(neighbors)):
        response = neighbors[x][-1]
        if response in votes:
            votes[response] += 1
        else:
            votes[response] = 1

    return votes


def getWeightedVote(neighbors, testinstance):
    votes = {}
    for x in range(len(neighbors)):
        response = neighbors[x][-1]
        if response in votes:
            votes[response] += 1 / (euclideanDistance(neighbors[x], testinstance, 1) + 0.1)  # avoid division by 0
        else:
            votes[response] = 1

    return votes


def getResponse(neighbors, testinstance, weighted=bool(0)):
    # Creating a list with all the possible neighbors
    if weighted == bool(1):
        votes = getWeightedVote(neighbors, testinstance)
    else:
        votes = getNormalVote(neighbors)

    if len(votes) > 1:
        print 'stop'
    sorted_votes = sorted(votes.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sorted_votes[0][0]


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

    split = 0.9995 #we use 0.0006% of the data to test
    loadDataset('accelerometer/1.csv', split, trainingSet, testSet)
    loadDataset('accelerometer/2.csv', split, trainingSet, testSet)
    # loadDataset('accelerometer/3.csv', split, trainingSet, testSet)
    # loadDataset('accelerometer/4.csv', split, trainingSet, testSet)
    # loadDataset('accelerometer/5.csv', split, trainingSet, testSet)
    #we avoid putting this into the training set
    loadDataset('accelerometer/3.csv', split, trainingSet1, custom_test)
    print 'Train set: ' + repr(len(trainingSet))
    print 'Test set: ' + repr(len(testSet))
    print 'Custom test set: ' + repr(len(custom_test))
    accuracy = []
    acc = 0
    ks = [3, 9, 21, 33, 66, 99]
    i = 0

    print('Custom test weighted knn!')
    for k in range(len(ks)):
        predictions = []
        i=0
        print ('k='+repr(ks[k]))
        for x in range(len(custom_test)):
            neighbors = getNeighbors(trainingSet, custom_test[x], ks[k])
            result = getResponse(neighbors, custom_test[x], bool(1))
            predictions.append(result)

            i+=1
            print(repr(++i) + '> predicted=' + repr(result) + ', actual=' + repr(custom_test[x][-1]))

        acc=getAccuracy(custom_test, predictions)
        accuracy.append(acc)
        print 'Custom Weighted Accuracy: ', acc

    # Plot the data
    x=ks
    y=accuracy
    plt.plot(x, y, label='Weighted KNN')
    plt.legend()
    plt.xlabel('K value')
    plt.ylabel('Accuracy %')

    print('Custom test normal knn!')
    accuracy = []
    for k in range(len(ks)):
        predictions = []
        i=0
        print ('k='+repr(ks[k]))
        for x in range(len(custom_test)):
            neighbors = getNeighbors(trainingSet, custom_test[x], ks[k])
            result = getResponse(neighbors, custom_test[x], bool(0))
            predictions.append(result)

            i+=1
            print(repr(++i) + '> predicted=' + repr(result) + ', actual=' + repr(custom_test[x][-1]))

        acc=getAccuracy(custom_test, predictions)
        accuracy.append(acc)
        print 'Custom Normal Accuracy: ', acc

    # Plot the data
    x=ks
    y=accuracy
    plt.plot(x, y, label='Normal KNN')
    plt.legend()
    plt.show()

main()