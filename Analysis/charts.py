#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build and show charts
"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
import csv
import pandas as pd
from pandas import DataFrame
from scipy.stats import chisquare

FILENAME = 'analysis_test.txt'
HEADERS=["Name", "Born", "Party", "Bundesland", "Gender", "Age", "Cluster 0", "Cluster 1", "Cluster 2", "Sum"]

class entry:
    def __init__(self, name, born, party, bundesland, gender, age, cl0, cl1, cl2, clsum):
        self.name = name.encode("utf-8")
        self.born = born
        self.party = party
        self.bundesland = bundesland
        self.gender = gender
        self.age = int(age)
        self.cl0 = int(cl0)
        self.cl1 = int(cl1)
        self.cl2 = int(cl2)
        self.clsum = int(clsum)
    def __repr__(self):
        return "{} {} {} {} {} {} {} {} {} {}".format(self.name, self.born, self.party, self.bundesland, self.gender, self.age, self.cl0, self.cl1, self.cl2, self.clsum)

def get_data(filename):
    data = []
    with open(FILENAME, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader, None) # Skip header
        for row in reader:
            data.append(entry(name=row[0], born=row[1], party=row[2], bundesland=row[3], gender=row[4], age=row[5], cl0=row[6], cl1=row[7], cl2=row[8], clsum=row[9]))
    return data

def make_pie(data):
    genders = {
        'Male': len([f for f in data if f.gender.lower() == 'male']),
        'Female': len([f for f in data if f.gender.lower() == 'female']),
    }
    gender_data = [genders[f] for f in genders.keys()]
    assert sum(gender_data) == len(data)
    colors = ['gold', 'yellowgreen']
    plt.pie(gender_data, labels=genders.keys(), colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.title('Gender Distribution')
    plt.show()

def pie_words(data):
    labels = 'Personal information', 'Political and economical information'
    sizes = [4376, 5656]
    colors = ['gold', 'yellowgreen']
    plt.pie(sizes, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.title('Proportion of clusters')
    plt.show()

def make_pie_state(data):
    bundesland = {
        'Hamburg': len([m for m in data if m.bundesland.lower() == 'hamburg']),
        'Niedersachsen': len([m for m in data if m.bundesland.lower() == 'niedersachsen']),
        'Bayern': len([m for m in data if m.bundesland.lower() == 'bayern']),
        'Saarland': len([m for m in data if m.bundesland.lower() == 'saarland']),
        'Schleswig-Holstein': len([m for m in data if m.bundesland.lower() == 'schleswig-holstein']),
        'Baden-Württemberg': len([m for m in data if m.bundesland.lower() == 'baden-württemberg']),
        'Nordrhein-Westfalen': len([m for m in data if m.bundesland.lower() == 'nordrhein-westfalen']),
        'Rheinland-Pfalz': len([m for m in data if m.bundesland.lower() == 'rheinland-pfalz']),
        'Hessen': len([m for m in data if m.bundesland.lower() == 'hessen']),
        'Mecklenburg-Vorpommern': len([m for m in data if m.bundesland.lower() == 'mecklenburg-vorpommern']),
        'Hessen': len([m for m in data if m.bundesland.lower() == 'hessen']),
        'Sachsen': len([m for m in data if m.bundesland.lower() == 'sachsen']),
        'Sachsen-Anhalt': len([m for m in data if m.bundesland.lower() == 'sachsen-anhalt']),
        'Bremen': len([m for m in data if m.bundesland.lower() == 'bremen']),
        'Berlin': len([m for m in data if m.bundesland.lower() == 'berlin']),
        'Brandenburg': len([m for m in data if m.bundesland.lower() == 'brandenburg']),
    }
    bundesland_data = [bundesland[m] for m in bundesland.keys()]
    assert sum(bundesland_data) == len(data)
    colors = ['gold', 'yellowgreen', 'coral', 'skyblue', 'purple' ]
    plt.pie(bundesland_data, labels=bundesland.keys(), colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.title('State Distribution')
    plt.show()

def make_pie_party(data):
     party = {
         'CDU': len([g for g in data if g.party.lower() == 'cdu']),
         'CSU': len([g for g in data if g.party.lower() == 'csu']),
         'Die Linke': len([g for g in data if g.party.lower() == 'die linke']),
         'no party': len([g for g in data if g.party.lower() == 'fraktionslos']),
         'Grüne': len([g for g in data if g.party.lower() == 'grüne']),
         'SPD': len([g for g in data if g.party.lower() == 'spd']),
     }
     party_data = [party[g] for g in party.keys()]
     assert sum(bundesland_data) == len(data)
     colors = ['gold', 'yellowgreen', 'coral', 'skyblue', 'purple', 'lime' ]
     plt.pie(party_data, labels=party.keys(), colors=colors,
             autopct='%1.1f%%', shadow=True, startangle=140)
     plt.axis('equal')
     plt.title('Party Distribution')

     plt.show()

def make_histogram(data):
    ages = [f.age for f in data]
    num_bins = 10
    n, bins, patches = plt.hist(ages, num_bins, facecolor='blue', alpha=0.5, edgecolor='black', linewidth=0.5)
    plt.xlim([20, 90])
    plt.title('Age Distribution')
    plt.ylabel('Number of politicians')
    plt.xlabel('Age')
    plt.show()

def make_histogram_words(data):
    numbers = [f.clsum for f in data]
    num_bins = 10
    n, bins, patches = plt.hist(numbers, num_bins, facecolor='silver', alpha=0.5, edgecolor='black', linewidth=0.5)
    plt.title('Number of unique search terms per politician')
    plt.ylabel('Number of politicians')
    plt.xlabel('Number of unique search terms')
    plt.show()

def make_plots(data):
    make_pie(data)
    pie_words(data)
    make_pie_state(data)
    make_histogram(data)
    make_histogram_words(data)
    make_pie_party(data)

def main():
    data = get_data(filename=FILENAME)
    make_plots(data=data)

if __name__ == "__main__":
    main()
