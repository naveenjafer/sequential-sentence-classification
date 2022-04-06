import json
import os
import sys
import jsonlines

inputFiles = ["dev.jsonl", "test.jsonl", "train.jsonl"]
outputFiles = ["dev_clean.txt", "test_clean.txt", "train_clean.txt"]

def process(inputPathDataset, outputPathDataset):
    data = []
    for indexFileName, file in enumerate(inputFiles):
        with jsonlines.open(os.path.join(inputPathDataset, file)) as f:
            for line in f.iter():
                for index, sentence in enumerate(line["sentences"]):
                    data.append(line["labels"][index] + "\t" + sentence)
                data.append("")
        
        with open(os.path.join(outputPathDataset, outputFiles[indexFileName]), "w") as f:
            for line in data:
                f.write(line)
                f.write("\n")



if __name__ == "__main__":
    inputPathDataset = sys.argv[1]
    outputPathDataset = sys.argv[2]
    if os.path.isdir(outputPathDataset) == False:
        os.mkdir(outputPathDataset)

    process(inputPathDataset, outputPathDataset)

