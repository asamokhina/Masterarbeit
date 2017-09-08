#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
utils.py

Utility functions
"""
import gensim
import string

FILENAME = 'pattern_output.txt'

def load_word_vectors(filename=FILENAME):
    print("Loading vectors from {}".format(filename))
    model = gensim.models.KeyedVectors.load_word2vec_format("german.model", binary=True)
    words = []
    with open(filename, "r", encoding="utf8") as f:
        words = f.readlines()
    words = [f.strip().title() for f in words]
    word_vectors = []
    used_words = []
    unused_words = []
    for b in words:
        if b in model:
            word_vectors.append(model[b])
            used_words.append(b)
        else:
            unused_words.append(b)
    print("Unused words: {}\nUsed words: {}".format(len(unused_words), len(used_words)))
    return (word_vectors, used_words, unused_words)

def clean_umlauts(input):
    return input.replace("ö", "oe").replace("ü", "ue").replace("ä", "ae")

def filter_characters(input):
    """
    Removes öüä from input, returns None if it contains a number, removes non-ascii characters
    """
    if any(c.isdigit() for c in input):
        return None
    acceptable_characters = string.ascii_letters + " "
    cleaned = clean_umlauts(input.lower().strip())
    filtered = "".join(list(filter(lambda c: c in acceptable_characters, cleaned)))
    if len(filtered) == 0:
        return None
    return filtered
