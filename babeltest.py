#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json
import pprint
import sys

pp = pprint.PrettyPrinter(depth=2)
WORDS = [


KEY="6c0e6287-e2e6-4ce7-a145-0f37f0300b7d"
r = requests.get('https://babelnet.io/v4/getVersion?key={}'.format(KEY))
print(r.text)

for word in WORDS:
    print("Looking up {}".format(word))
    r = requests.get('https://babelnet.io/v4/getSynsetIds?key={}&langs=DE&word={}'.format(KEY, word))
    response = json.loads(r.text)
    for id in response:
        r = requests.get('https://babelnet.io/v4/getSynset?key={}&id={}&filterLangs=DE'.format(KEY, id['id']))
        synset = json.loads(r.text)
        print(json.dumps(synset['categories']))
        