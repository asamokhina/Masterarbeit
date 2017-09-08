#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Get training data from the file and perform text classification, evaluate the results
"""
from sklearn import svm
import csv
from utils import clean_umlauts
import numpy as np
import argparse
from sklearn.model_selection import cross_val_score
VECTOR_FILE = "word_vectors_t.csv"
CLUSTER_FILE = "word_clusters_t.csv"
OUTPUT_FILE = "svm_output.csv"
INPUT_WORDS_FILE = "classification_input.csv"
class Word:
    def __init__(self, word, vectors=[]):
        self.word = word
        self.vectors = np.asarray(vectors, dtype=np.float64)
        self.cluster = -1
    def __repr__(self):
        return "{} in cluster {}".format(self.word, self.cluster)
    def __eq__(self, other):
        return self.cluster == other.cluster and self.word == other.word

def setup_classifier(words):
    clf = svm.SVC()
    n_features = len(words[0].vectors)
    n_samples = len(words)
    training_set = np.asarray([f.cluster for f in words], dtype=np.int16)
    input_vectors = np.asarray([f.vectors for f in words])
    clf.fit(X=input_vectors, y=training_set)
    scores = cross_val_score(clf, input_vectors, training_set)
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    return clf

def classify(classifier, input):
    return classifier.predict(np.asarray([f.vectors for f in input]))

def load_vectors(filename=VECTOR_FILE):
    print("Loading vectors from {}".format(filename))
    vectors = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            vectors.append(Word(row[0],  row[1:]))
    return vectors

def load_clusters_with_word_array(filename=CLUSTER_FILE, words=[]):
    print("Loading clusters from {}".format(filename))
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            for word in words:
                if word.word == row[0]:
                    word.cluster = row[1]
                    break


def load_words(vector_file, cluster_file):
    words = load_vectors(filename=vector_file)
    load_clusters_with_word_array(filename=cluster_file, words=words)
    print("Loaded {} words".format(len(words)))
    return words

def check_words(words):
    unclustered = [f for f in words if f.cluster == -1]
    if len(unclustered) > 0:
        raise Exception("Unclustered data found")

def parse_args():
    parser = argparse.ArgumentParser(description='Classify words.')
    parser.add_argument("--input", default=INPUT_WORDS_FILE, type=str, help="Input file to be classified")
    parser.add_argument("--clusters", default=CLUSTER_FILE, type=str, help="Training data containing cluster assignments")
    parser.add_argument("--vectors", default=VECTOR_FILE, type=str, help="Training data containing word vectors")
    parser.add_argument("--output", default=OUTPUT_FILE, type=str, help="Destination file for classified clusters")
    args = parser.parse_args()
    return args

def main():
    """
    Main
    """
    args = parse_args()
    training_words = load_words(cluster_file=args.clusters, vector_file=args.vectors)
    check_words(training_words)
    input_vectors = load_vectors(filename=args.input)
    print("Loaded {} words for input".format(len(input_vectors)))
    classifier = setup_classifier(training_words)
    output = classify(classifier, input_vectors)
    for i, j in enumerate(input_vectors):
        j.cluster = output[i]

    print("Writing classification output to {}".format(args.output))
    with open(args.output, "w", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for word in input_vectors:
            writer.writerow([word.word, word.cluster])

if __name__ == "__main__":
    main()
