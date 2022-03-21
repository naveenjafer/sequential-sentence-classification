# takes an input file and converts it into a non contextualized format.

import os
import sys

def nonContextualize(inputFileName, outputFileName):
    dataFile = []
    with open(inputFileName) as f:
        while True:
            line = f.readline()
            if len(line.split("\t")) == 2:
                dataFile.append(line.split("\t"))
            if not line:
                break
    
    print("len of file", len(dataFile))
    with open(outputFileName, "w") as f:
        for item in dataFile:
            print(item[0])
            f.write(item[0] + "\t" + item[1])
            f.write('\n')
    f.close()

if __name__ == "__main__":
    print("came here")
    inputFileName = sys.argv[1]
    outputFileName = sys.argv[2]
    print("here too")
    nonContextualize(inputFileName, outputFileName)