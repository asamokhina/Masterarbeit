#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
word_vectorise.py
"""

from utils import load_word_vectors
import numpy as np
import argparse
import csv

def parse_args():
    parser = argparse.ArgumentParser(description='Vectorises words.')
    parser.add_argument("--input", type=str, required=True, help="Input file to be vectorised")
    parser.add_argument("--output", type=str, required=True, help="Vector output CSV file")
    args = parser.parse_args()
    return args


def main():
    """
    Open csv
    """
    args = parse_args()
    word_vectors, used_words, unused_words = load_word_vectors(args.input)

    with open(args.output, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for i, word in enumerate(used_words):
            vectors = word_vectors[i]
            writer.writerow([word,] + vectors.tolist())

if __name__ == "__main__":
    main()
