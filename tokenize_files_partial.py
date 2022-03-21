"""Tokenizes the sentences with BertTokenizer as tokenisation costs some time.
"""

from transformers import BertTokenizer
import sys

BERT_VOCAB = "bert_model/scibert_scivocab_uncased/vocab.txt"
#BERT_VOCAB = "yihanlin/scibert_scivocab_uncased"
MAX_SEQ_LENGTH = 128


def tokenize_file(in_file, out_file, tokenizer):
    with open(in_file, encoding="utf-8") as in_f:
        with open(out_file, encoding="utf-8", mode="w") as out_f:
            for line in in_f:
                line = line.replace("\r", "")
                if line.strip() == "" or line.startswith("###"):
                    out_f.write(line + "\n")
                else:
                    ls = line.split("\t")
                    tag, sentence = ls[0], ls[1]
                    tokenized = tokenizer.encode(sentence, add_special_tokens=True, max_length=MAX_SEQ_LENGTH)
                    out_f.write(f'{tag}\t{" ".join([str(t) for t in tokenized])}\n')


def tokenize(dataset):
    tokenizer = BertTokenizer.from_pretrained(BERT_VOCAB, do_lower_case=True)
    

    if "nicta-piboso" in dataset or "pubmed-20k" in dataset or "CSAbstruct" in dataset:
        print(dataset)
        tokenize_file("datasets/" + dataset + "/train_clean.txt", "datasets/" + dataset + "/train_scibert.txt", tokenizer)
        tokenize_file("datasets/" + dataset + "/dev_clean.txt", "datasets/" + dataset + "/dev_scibert.txt", tokenizer)
        tokenize_file("datasets/" + dataset + "/test_clean.txt", "datasets/" + dataset + "/test_scibert.txt", tokenizer)



if __name__ == "__main__":
    dataset = sys.argv[1]
    tokenize(dataset)