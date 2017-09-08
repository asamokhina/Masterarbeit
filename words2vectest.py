#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
words2vectest.py
"""

import gensim
import time
from sklearn.cluster import KMeans
from sklearn import metrics
from utils import load_word_vectors
from sklearn import svm
import numpy as np
import csv
FILENAME = 'pattern_single_word_output.txt'
VECTOR_OUTPUT_FILE = "word_vectors.csv"
CLUSTER_OUTPUT_FILE = "word_clusters.csv"
def main():
    """
    Open csv
    """

    word_vectors, used_words, unused_words = load_word_vectors(FILENAME)

    start = time.time()
    n_clusters = 3

    print("Clustering")
    kmeans_clustering_predict = KMeans(n_clusters=n_clusters)
    idx = kmeans_clustering_predict.fit_predict(word_vectors)
    clustered_words = {}
    for index, cluster in enumerate(idx):
        key = used_words[index]
        if key not in clustered_words:
            clustered_words[key] = cluster
        else:
            raise Exception("Key {} already exists!".format(key))

    kmeans_clustering = kmeans_clustering_predict.fit(word_vectors)
    labels = kmeans_clustering.labels_
    metrics.silhouette_score(word_vectors, labels, metric='euclidean')
    metrics.calinski_harabaz_score(word_vectors, labels)

    end = time.time()
    elapsed = end - start
    print ("Time taken for clustering: {} seconds.".format(elapsed))
    print ("Silhouette score: {}".format(metrics.silhouette_score(word_vectors, labels, metric='euclidean')))
    print ("CH score: {}".format(metrics.calinski_harabaz_score(word_vectors, labels)))

    print("Saving word clusters to {}".format(CLUSTER_OUTPUT_FILE))
    with open(CLUSTER_OUTPUT_FILE, "w", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for clustered_word, cluster in clustered_words.items():
            writer.writerow([clustered_word, cluster])
    with open("wordsNOTvec_output.txt", "w", encoding="utf8") as f:
        for unused_word in unused_words:
            f.write(unused_word + "\n")
    print("Saving word vectors to {}".format(VECTOR_OUTPUT_FILE))

    with open(VECTOR_OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for i, word in enumerate(used_words):
            vectors = word_vectors[i]
            writer.writerow([word,] + vectors.tolist())

if __name__ == "__main__":
    main()
