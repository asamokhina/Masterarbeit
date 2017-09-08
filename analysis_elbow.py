#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Get data from file and compare silhuette scores to alocate the best cluster number
"""

import time
from sklearn.cluster import KMeans
from sklearn import metrics
from sklearn import preprocessing
from scipy.spatial.distance import cdist, pdist
import matplotlib.pyplot as plt
import numpy as np
from pandas import factorize
from sklearn import metrics
from kmodes import kprototypes
import csv

FILENAME = 'analysis_kmodes.csv'
HEADERS=["Name", "Party", "Gender", "Group", "Cluster 0", "Cluster 2"]
CLUSTER_OUTPUT_FILE = "final_clusters.csv"

class entry:
    def __init__(self, name, party, gender, age, cl0, cl2):
        self.name = name.encode("utf-8")
        self.party = party
        self.gender = gender
        self.age = int(age)
        self.cl0 = int(cl0)
        self.cl2 = int(cl2)
    def __repr__(self):
        return "{} {} {} {} {} {}".format(self.name, self.party, self.gender, self.age, self.cl0, self.cl2)

def get_data(filename):
    data = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader, None) # Skip header
        for row in reader:
            data.append(entry(name=row[0], party=row[1], gender=row[2], age=row[3], cl0=row[4], cl2=row[5]))
    return data



def main():
    """
    Create a range of clusters and compare them
    """

    start = time.time()
    n_clusters = range(2, 9)
    print("Using cluster sizes from {} to {}".format(min(n_clusters), max(n_clusters)))
    raw_data = get_data(FILENAME)
    data = np.empty((len(raw_data),5))
    data[:,0], _ = factorize([f.party for f in raw_data])
    data[:,1], _ = factorize([f.gender for f in raw_data])
    data[:,2] = preprocessing.scale([f.age for f in raw_data])
    data[:,3] = preprocessing.scale([f.cl0 for f in raw_data])
    data[:,4] = preprocessing.scale([f.cl2 for f in raw_data])
    print("Clustering", len(data), "entries")

    sil_scores = []
    for n in n_clusters:
        print(n, "clusters")
        kproto = kprototypes.KPrototypes(n_clusters=n).fit(X=data, categorical=[0,1])
        labels = kproto.labels_
        score = metrics.silhouette_score(data, labels, metric='cosine')
        sil_scores.append(np.array([n, score]))
        print ("Silhouette score: {}".format(score))
    sil_scores = np.array(sil_scores)
    plt.plot(sil_scores[:,0], sil_scores[:,1], color='k')
    plt.ylabel('Silhouette score')
    plt.xlabel('Number of clusters')
    plt.show()

if __name__ == "__main__":
    main()
