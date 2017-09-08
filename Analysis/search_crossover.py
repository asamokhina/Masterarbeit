#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calculates search crossover
"""
import sys
sys.path.append('..') # Search parent directory for modules too
from utils import clean_umlauts
import csv

def read_csv(filename):
    data = []
    with open(filename) as file:
        data = [clean_umlauts(f.lower().strip().replace('"', '')) for f in file.readlines()]
    return data

def calc_relative(intersection, total):
    return "{0:.2f}%".format(intersection / total * 100)

def main():
    all_bing = set(read_csv(filename='../all_bing.csv'))
    all_google = set(read_csv(filename='../all_google.csv'))
    all_ddg = set(read_csv(filename='../all_ddg.csv'))

    bing_google = len(all_bing.intersection(all_google))
    bing_ddg = len(all_bing.intersection(all_ddg))
    google_ddg = len(all_google.intersection(all_ddg))

    total_bing = len(all_bing)
    total_ddg = len(all_ddg)
    total_google = len(all_google)

    print("Absolute intersection:")
    print("----------------------")
    print("Bing-Google:", bing_google)
    print("Bing-DDG:", bing_ddg)
    print("Google-DDG:", google_ddg)
    print("")
    print("Relative intersection")
    print("----------------------")

    bing_google_rel_bing = calc_relative(bing_google, total_bing)
    bing_google_rel_google = calc_relative(bing_google, total_google)

    bing_ddg_rel_bing =  calc_relative(bing_ddg, total_bing)
    bing_ddg_rel_ddg =  calc_relative(bing_ddg, total_ddg)

    google_ddg_rel_google =  calc_relative(google_ddg, total_google)
    google_ddg_rel_ddg =  calc_relative(google_ddg, total_ddg)

    print("Bing-Google overlap relative to Bing:\t", bing_google_rel_bing, "–", bing_google, "of",  total_bing )
    print("Bing-Google overlap relative to Google:\t", bing_google_rel_google, "–", bing_google, "of",  total_google )
    print("Bing-DDG overlap relative to Bing:\t", bing_ddg_rel_bing, "–", bing_ddg, "of",  total_bing )
    print("Bing-DDG overlap relative to DDG:\t", bing_ddg_rel_ddg, "–", bing_ddg, "of",  total_ddg )
    print("Google-DDG overlap relative to Google:\t", google_ddg_rel_google, "–", google_ddg, "of",  total_google )
    print("Google-DDG overlap relative to DDG:\t", google_ddg_rel_ddg, "–", google_ddg, "of",  total_ddg )

if __name__ == "__main__":
    main()
