import sys
import random

def positionOnly(inputFileName, outputFileName):
    dataFile = []
    with open(inputFileName) as f:
        dataLocal = []
        while True:
            
            line = f.readline()
            if len(line.split("\t")) < 2:
                dataFile.append(dataLocal)
                dataLocal = []
            if not line:
                break
            dataLocal.append(line.split("\t"))
    

    
    with open(outputFileName, "w") as f:
        for item in dataFile:
            for index, content in enumerate(item):
                print(content)
                if len(content) == 2:
                    f.write(content[0] + "\t" + str(index))
            f.write('\n')
    
    print("[done messing up - ", inputFileName, "]")

if __name__ == "__main__":
    inputFileName = sys.argv[1]
    outputFileName = sys.argv[2]

    positionOnly(inputFileName, outputFileName)