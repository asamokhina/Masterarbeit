#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Allocates cluster numbers to search terms then outputs the amount of each cluster each search term has.

Run me with the following example command line:

python3 allocate_clusters.py  --clusters full_test.csv --searchterms search_terms_with_suggestion.csv --output CHANGEME.csv --sourcefile bundestag.csv
"""

import csv
import argparse
from utils import clean_umlauts, filter_characters

class SearchTerm():
    def __init__(self, search_term, result):
        self.search_term = search_term
        self.result = filter_characters(result)
        self.cluster = -1
    def __repr__(self):
        return "{}: {} ({})".format(self.search_term, self.result, self.cluster)
    def to_array(self):
        return [self.search_term, self.result, self.cluster]

class ClusterAllocation():
    def __init__(self, word, cluster):
        self.word = filter_characters(word)
        self.cluster = int(cluster)
    def __repr__(self):
        return "{}: {}".format(self.word, self.cluster)

class Politician():
    def __init__(self, name, born, party, area, gender, age):
        self.name = name
        self.born = born
        self.party = party
        self.area = area
        self.gender = gender
        self.age = age
        self.cluster_dict = {}
    def to_array(self):
        return [self.name, self.born, self.party, self.area, self.gender, self.age]

def load_csv(filename, action, delimiter=',', skip_header=False):
    print("Loading", filename)
    data = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)
        if skip_header:
            next(reader)
        for row in reader:
            entry = action(row)
            if entry is not None:
                data.append(entry)
    return data

def _load_search_csv_entry(entry):
    return SearchTerm(search_term=entry[0], result=entry[1])

def _load_cluster_csv_entry(entry):
    return ClusterAllocation(word=entry[0], cluster=entry[1])

def _load_source_csv_entry(entry):
    return Politician(name=entry[0], born=entry[1], party=entry[2], area=entry[3], gender=entry[4], age=entry[5])


def load_search_csv(filename):
    return load_csv(filename=filename, action=_load_search_csv_entry)

def load_cluster_csv(filename):
    return load_csv(filename=filename, action=_load_cluster_csv_entry)

def load_source_csv(filename):
    return load_csv(filename=filename, action=_load_source_csv_entry, skip_header=True)

def parse_args():
    parser = argparse.ArgumentParser(description='Allocates cluster numbers to search terms.')
    parser.add_argument("--clusters", type=str, required=True, help="CSV file containing cluster allocations")
    parser.add_argument("--searchterms", type=str, required=True, help="CSV file containing original search terms")
    parser.add_argument("--sourcefile", type=str, required=True, help="Source file containing original search terms and metadata")
    parser.add_argument("--output", type=str, required=True, help="Output CSV file")
    args = parser.parse_args()
    return args


def write_result(filename, results, num_clusters):
    with open(filename, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Name", "Born", "Party", "Bundesland", "Gender", "Age"] + ["Cluster {}".format(f) for f in range(num_clusters)])
        for f in results:
            writer.writerow(f.to_array() + [f.cluster_dict[g] for g in range(0, num_clusters)])

def uniquify_search_terms(search_terms):
    return set([f.search_term for f in search_terms])

def main():
    args = parse_args()

    clusters = load_cluster_csv(filename=args.clusters)
    search_terms = load_search_csv(filename=args.searchterms)
    politicians = load_source_csv(filename=args.sourcefile)
    num_clusters = max([f.cluster for f in clusters]) + 1
    unique_search_terms = uniquify_search_terms(search_terms)

    print("There are", len(clusters), "clustered words.")
    print("There are", len(politicians), "politicians")


    print("There are", len(search_terms), "search term pairs.")
    print("There are", len(unique_search_terms), "unique search terms.")

    politican_names = [g.name for g in politicians]
    filtered_search_terms = [
        f for f in search_terms
        if f.search_term in politican_names
    ]

    unique_filtered_search_terms = uniquify_search_terms(filtered_search_terms)

    print("There are", len(filtered_search_terms), "search term pairs after filtering those not found in the source list of politicians.")
    print("There are", len(unique_filtered_search_terms), "unique filtered search terms.")

    print("Found", num_clusters, "clusters.")
    clustered_search_terms = []
    for search_term in filtered_search_terms:
        for cluster in clusters:
            if search_term.result == cluster.word:
                search_term.cluster = cluster.cluster
                clustered_search_terms.append(search_term)
                break
    for politician in politicians:
        politician.search_terms = [f for f in clustered_search_terms if f.search_term == politician.name]
        #print(politician.name,"has",len(politician.search_terms), "search terms associated")
        for i in range(0, num_clusters):
            politician.cluster_dict[i] = len([f for f in politician.search_terms if f.cluster == i])
    print("There are", len(clustered_search_terms), "search term pairs with a clustered result.")

    write_result(results=politicians, filename=args.output, num_clusters=num_clusters)

if __name__ == "__main__":
    main()
