#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
import sys
# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('utf-8')
from pattern.web import decode_utf8
from pattern.de import parse
from pattern.de import singularize, pluralize
from pattern.de import conjugate
from pattern.de import INFINITIVE, PRESENT, SG, SUBJUNCTIVE
from pattern.de import attributive, predicative
from pattern.de import MALE, FEMALE, SUBJECT, OBJECT
from pattern.de import parse, split
from pattern.de import tag
import requests
import json
import pprint
import io
import argparse
import string
from utils import clean_umlauts

FILENAME = 'test3007.csv'
OUTPUT_FILENAME = "pattern_output.txt"
OUTPUT_SINGLE_FILENAME = "pattern_single_word_output.txt"

def parse_args():
    parser = argparse.ArgumentParser(description='Normalise words.')
    parser.add_argument("--input", default=FILENAME, type=str, help="Input file to be processed")
    parser.add_argument("--output", default=OUTPUT_FILENAME, type=str, help="Output file")
    parser.add_argument("--singleoutput", default=OUTPUT_SINGLE_FILENAME, type=str, help="Output file (only single word entries)")
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    words = []
    print("Loading from {}".format(args.input))
    with io.open(args.input,encoding='utf8') as f:
        acceptable_characters = string.letters + string.digits + " äüö"
        for line in f.readlines():
            if line.strip() == "suggestterm":
                continue
            word = filter(lambda c: c in acceptable_characters, line).strip()
            if len(word) > 0 and not any(c.isdigit() for c in word):
                words.append(word)

    print("Parsing {} words".format(len(words)))
    parsed_words = []
    for f in words:
        parsed = parse(f, tags=False, chunks=False, relations=False, lemmata=True)
        parsedlist = u" ".join([word.split("/")[2] for word in parsed.split(" ")])
        parsed_words.append(parsedlist)

    print("Saving {} words to {}".format(len(parsed_words), args.output))
    with open(args.output, "w") as f:
        for word in parsed_words:
            print(clean_umlauts(word), file=f)

    single_word_entries = list({clean_umlauts(f.strip()) for f in parsed_words if " " not in f})
    single_word_entries.sort()
    print("Saving {} words to {}".format(len(single_word_entries), args.singleoutput))
    with open(args.singleoutput, "w") as f:
        for word in single_word_entries:
            print(word, file=f)


if __name__ == "__main__":
    main()
