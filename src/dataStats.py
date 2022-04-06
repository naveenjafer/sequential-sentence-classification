import os
import json
import sys
from collections import defaultdict
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

def plotLabelFreqStats(labels_df):
    sns.countplot(x = "label", data = labels_df)
    plt.show()

def plotSentenceLengthStats(labels_df):
    sns.boxplot(x="label", y="sent_length", data=labels_df)
    plt.show()

def plotConfusionMatrix(result,labelSet):
    sns.heatmap(result,annot=True,annot_kws = {'size':8}, xticklabels=labelSet, yticklabels=labelSet, square=True)
    plt.show()

def normalizeCFMatrix(suffixResult):
    tot = sum(sum(suffixResult,[]))
    suffixResult = [[i/tot*100 for i in row] for row in suffixResult]
    return suffixResult

def plotSuffixPrefixStats(dataFile, labelSet):
    suffixResult = [[0 for i in range(len(labelSet))] for j in range(len(labelSet))]
    prefixResult = [[0 for i in range(len(labelSet))] for j in range(len(labelSet))]
    suffixResultTransitions = [[0 for i in range(len(labelSet))] for j in range(len(labelSet))]
    breakTypeResult = [[0 for i in range(len(labelSet))] for j in range(len(labelSet))]
    labelIndexMap = {}
    for index, label in enumerate(labelSet):
        labelIndexMap[label] = index

    
    for paper in dataFile:
        for index, record in enumerate(paper):
            if index < len(paper)-1:
                suffixResult[labelIndexMap[record[0]]][labelIndexMap[paper[index+1][0]]] += 1
                if labelIndexMap[record[0]] != labelIndexMap[paper[index+1][0]]:
                    suffixResultTransitions[labelIndexMap[record[0]]][labelIndexMap[paper[index+1][0]]] += 1
            if index > 0:
                prefixResult[labelIndexMap[record[0]]][labelIndexMap[paper[index-1][0]]] += 1

            if index < len(paper)-1 and index > 0:
                if labelIndexMap[paper[index-1][0]] == labelIndexMap[paper[index+1][0]] and labelIndexMap[record[0]] != labelIndexMap[paper[index-1][0]]:
                    breakTypeResult[labelIndexMap[paper[index-1][0]]][labelIndexMap[record[0]]] += 1
            
    
    suffixResult = normalizeCFMatrix(suffixResult)
    prefixResult = normalizeCFMatrix(prefixResult)
    suffixResultTransitions = normalizeCFMatrix(suffixResultTransitions)
    breakTypeResult = normalizeCFMatrix(breakTypeResult)
    plotConfusionMatrix(suffixResult, labelSet)
    plotConfusionMatrix(prefixResult, labelSet)
    plotConfusionMatrix(suffixResultTransitions, labelSet)
    plotConfusionMatrix(breakTypeResult, labelSet)

def getLabelStats(dataFile):
    labelSet = set()
    labelDfBuilder = []
    labelCounter = {}
    for paper in dataFile:
        for record in paper:
            labelDfBuilder.append([record[0], len(record[1])])
            labelSet.add(record[0])
            if record[0] not in labelCounter:
                labelCounter[record[0]] = 1
            else:
                labelCounter[record[0]] += 1

    labels_df = pd.DataFrame(labelDfBuilder, columns = ['label', 'sent_length'])
    return labels_df, labelSet, labelCounter
    
def cleanup(dataFile):
    for index,paper in enumerate(dataFile):
        paper = [item for item in paper if len(item)==2]
        dataFile[index] = paper
    return dataFile

def generateGraphs(dataFile, labels_df, labelSet):
    plotLabelFreqStats(labels_df)
    plotSentenceLengthStats(labels_df)
    plotSuffixPrefixStats(dataFile, list(labelSet))

def getFileData(fileName):
    dataFile = []
    counterStats = {"total" : 0, "average_sent_per_doc" : 0, "vocab" : set()}
    with open(fileName) as f:
        dataLocal = []
        while True:
            
            line = f.readline()
            if len(line.split("\t")) < 2:
                dataFile.append(dataLocal)
                #replace this later with a tokenizer
                
                for entry in dataLocal:
                    if len(entry) > 1:
                        for token in entry[1].split(" "):
                            counterStats["vocab"].add(token)
                counterStats["average_sent_per_doc"] += len(dataLocal)
                dataLocal = []
            if not line:
                break
            counterStats["total"] += 1
            dataLocal.append(line.split("\t"))

    dataFile = cleanup(dataFile)
    print("Number of sentences: ")
    print(len(dataFile))
    print("Average len of each doc:" , counterStats["average_sent_per_doc"]/len(dataFile))
    print("Total sentences:", counterStats["total"])
    print("Vocab size: ", len(counterStats["vocab"]))
    #quit(1)
    return dataFile

def analyze(fileName):
    dataFile = getFileData(fileName)
    #print(len(dataFile[0]))
    labels_df, labelSet, _ = getLabelStats(dataFile)
    generateGraphs(dataFile, labels_df, labelSet)
    
if __name__ == "__main__":
    fileName = sys.argv[1]
    analyze(fileName)

    

