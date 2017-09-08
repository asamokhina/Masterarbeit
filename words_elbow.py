#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Get data from file and compare average within-cluster sum of squares to alocate the best cluster number
"""

import time
from sklearn.cluster import KMeans
from sklearn import metrics
from scipy.spatial.distance import cdist, pdist
from utils import load_word_vectors
import matplotlib.pyplot as plt
import numpy as np
FILENAME = 'pattern_single_word_output.txt'

def plot_elbow_curve(n_clusters, avgWithinSS, bss, tss):
    """
    Plots an elbow curve
    """
    # elbow curve
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(n_clusters, avgWithinSS, 'b*-', color='k')
    #ax.plot(n_clusters[kIdx], avgWithinSS[kIdx], marker='o', markersize=12,
    #markeredgewidth=2, markeredgecolor='r', markerfacecolor='None')
    plt.grid(True)
    plt.xlabel('Number of clusters')
    plt.ylabel('Average within-cluster sum of squares')
    plt.title('Elbow for KMeans clustering')

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(n_clusters, bss/tss*100, 'b*-', color='k')
    plt.grid(True)
    plt.xlabel('Number of clusters')
    plt.ylabel('Percentage of variance explained')
    plt.title('Elbow for KMeans clustering')

    plt.show()

def main():
    """
    Create a range of clusters and compare them
    """
    word_vectors, used_words, unused_words = load_word_vectors(FILENAME)
    start = time.time()
    n_clusters = range(1, 21)
    print("Using cluster sizes from {} to {}".format(min(n_clusters), max(n_clusters)))
    kmeans_clusters = [KMeans(n_clusters=n).fit(word_vectors) for n in n_clusters]
    centroids = [k.cluster_centers_ for k in kmeans_clusters]

    D_k = [cdist(word_vectors, cent, 'euclidean') for cent in centroids]
    cIdx = [np.argmin(D, axis=1) for D in D_k]
    dist = [np.min(D, axis=1) for D in D_k]
    avgWithinSS = [sum(d) / len(word_vectors) for d in dist]

    # Total with-in sum of square
    wcss = [sum(d**2) for d in dist]
    tss = sum(pdist(word_vectors)**2)/len(word_vectors)
    bss = tss-wcss

    stop = time.time()
    print("Time taken for clustering: {} seconds.".format(stop - start))

    print("Plotting elbow curve")
    plot_elbow_curve(n_clusters=n_clusters, avgWithinSS=avgWithinSS, bss=bss, tss=tss)

if __name__ == "__main__":
    main()
