#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Get data from file, build a cluster model and calculate Silhouette score
"""

from sklearn.cluster import KMeans
from sklearn import metrics
from sklearn import preprocessing
from scipy.spatial.distance import cdist, pdist
import matplotlib.pyplot as plt
import numpy as np
from sklearn import metrics
from utils import load_word_vectors
from pandas import factorize
from kmodes import kprototypes
import csv
FILENAMENAMES = 'names.txt'
FILENAME = 'analysis_kmodes.csv'
HEADERS=["Name", "Party", "Gender", "Age", "Cluster 0", "Cluster 2"]
CLUSTER_OUTPUT_FILE = "final_clusters2.csv"

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
    def to_row(self):
        return [
            self.name.decode("utf-8"),
            self.party,
            self.gender,
            self.age,
            self.cl0,
            self.cl2,
        ]

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
    Create a cluster model
    """
    print("Clustering")
    raw_data = get_data(FILENAME)
    data = np.empty((len(raw_data),5))
    n_clusters=2
    data[:,0], _ = factorize([f.party for f in raw_data])
    data[:,1], _ = factorize([f.gender for f in raw_data])
    data[:,2] = preprocessing.scale([f.age for f in raw_data])
    data[:,3] = preprocessing.scale([f.cl0 for f in raw_data])
    data[:,4] = preprocessing.scale([f.cl2 for f in raw_data])
    print("Clustering", len(data), "entries")
    kproto = kprototypes.KPrototypes(n_clusters=n_clusters).fit(X=data, categorical=[0,1])
    idx = kproto.fit_predict(data, categorical=[0,1])
    labels = kproto.labels_
    silohouette = metrics.silhouette_score(data, labels, metric='cosine')

    print ("Silhouette score: {}".format(silohouette))

    print("Saving word clusters to {}".format(CLUSTER_OUTPUT_FILE))
    with open(CLUSTER_OUTPUT_FILE, "w", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Name", "Party", "Gender", "Age", "Cluster 0", "Cluster 2", "Assigned Cluster"])
        for i, j in enumerate(raw_data):
            writer.writerow(j.to_row() + [labels[i],])




if __name__ == "__main__":
    main()
