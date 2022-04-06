import json
import os
import sys
import dataStats
from csv import reader
import externalStats
import utils
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def getF1ByClass(resultsFolder):
    labelF1Counter = {}
    with open(os.path.join(resultsFolder, "f1_per_label.csv")) as read_obj:
        csv_reader = reader(read_obj)
        header = next(csv_reader)
        if header != None:
            for row in csv_reader:
                labelF1Counter[row[3]] = row[4]
    return labelF1Counter

def normalizeDict(labelCounter):
    valTot = 0
    for key in labelCounter:
        valTot += labelCounter[key]
    
    for key in labelCounter:
        labelCounter[key] = round(labelCounter[key]*100/valTot,2)

    return labelCounter

def plotChart(labelF1Counter,kappaCounter, labelCounter, resultsFolder):
    f1scoresList, kappaList, freqList, labelsList = [], [], [], []
    for key in labelF1Counter:
        f1scoresList.append(labelF1Counter[key])
        kappaList.append(kappaCounter[key])
        freqList.append(labelCounter[key])
        labelsList.append(key)

    df = pd.DataFrame({"f1scores" : f1scoresList, "kappaList" : kappaList, "freqList" : freqList, "labelsList": labelsList})

    fig, ax = plt.subplots()
    size_scaler = 100 # Your points will be too small if you just use sd
    ax.scatter(np.arange(len(df['labelsList'])), df['f1scores'], s=df['freqList']*size_scaler, c=df['kappaList'], cmap = 'Blues', marker='o')
    ax.xaxis.set_ticks(np.arange(len(df['labelsList'])))
    ax.xaxis.set_ticklabels(df['labelsList'], rotation="horizontal", fontsize=4)
    #plt.figure(figsize=(10, 10))
    #plt.colorbar()
    plt.xlabel("classes",rotation="horizontal",fontsize=2)
    plt.ylabel("f1 score")
    plt.savefig(os.path.join(resultsFolder, "f1-freq-labels-chart.png"))



def freq_f1_comparisions(dataFileName, resultsFolder):
    dataFile = dataStats.getFileData(dataFileName)
    labels_df, labelSet, labelCounter = dataStats.getLabelStats(dataFile)
    labelCounter = normalizeDict(labelCounter)

    labelF1Counter = getF1ByClass(resultsFolder)
    labelF1Counter = {key : round(float(labelF1Counter[key]),2) for key in labelF1Counter}
    kappaCounter = externalStats.ART_KOHEN_KAPPA

    unifiedDfList = []
    print(labelF1Counter)
    print(kappaCounter)
    print(labelCounter)
    
    for key in kappaCounter:
        unifiedDfList.append([key, str(kappaCounter[key]), str(labelF1Counter[key]), str(labelCounter[key])])

    unifiedDf = pd.DataFrame(unifiedDfList, columns = ['class', 'Kohen Kappa', 'F1 score', 'Freq'])

    print (unifiedDf)
    #utils.save_df_as_image(unifiedDf, os.path.join(resultsFolder, "freq-f1-kohen.png"))
    plotChart(labelF1Counter, kappaCounter, labelCounter, resultsFolder)

if __name__ == "__main__":
    dataFileName = sys.argv[1]
    resultsFolder = sys.argv[2]
    
    freq_f1_comparisions(dataFileName, resultsFolder)
    #datasetStats()


