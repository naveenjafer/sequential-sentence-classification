import sys
import random

def shuffle(inputFileName, outputFileName):
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
    
    for index, item in enumerate(dataFile):
        random.shuffle(item)
        dataFile[index] = item
    
    with open(outputFileName, "w") as f:
        for item in dataFile:
            for content in item:
                print(content)
                if len(content) == 2:
                    f.write(content[0] + "\t" + content[1])
            f.write('\n')
    
    print("[done shuffling - ", inputFileName, "]")

if __name__ == "__main__":
    inputFileName = sys.argv[1]
    outputFileName = sys.argv[2]

    shuffle(inputFileName, outputFileName)