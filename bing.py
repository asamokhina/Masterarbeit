#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crawls the Bing API for autocomplete terms
"""

from time import sleep
import random
import datetime
from timeit import default_timer as timer
import re
import sys
import argparse
import threading
import pymysql.cursors
import requests
from crawl_utils import *

# global variables
HEADERS = {'User-agent':'Mozilla/5.0'}
URL = 'http://api.bing.net/osjson.aspx'
LANGUAGES = ['de-DE'] # ['de-DE', 'en-GB']
MAX_RETRIES = range(5)
TIMEOUT = 1

LOGFILE, LOG = init_logging('crawler_bing.log')

def log_error(message):
    """
    Outputs a log entry to both the stderr logger and the file logger
    """
    LOG.error(message)
    LOGFILE.error(message)

def query_bing_suggest(query, lang):
    """
    Sends an HTTP request to the Bing autocomplete API and returns the raw data
    returend by the API.
    """
    params = {'Market': lang, 'query': query}
    return send_request(LOG, URL, MAX_RETRIES, params, HEADERS, TIMEOUT)

def get_suggestion_terms(request_data, queryterm):
    """
    Parses the raw request_data as JSON and extracts the suggestions.

    Data returned from the Bing API is formatted like so:

    [
        "Angel Merkel",
        [
            "angela merkel",
            "angel merkels abgekaute fingernägel",
            "angela merkel wiki",
            "angel merkel falten",
            "angela merkels mann",
            "angel merkel humor"
        ]
    ]

    Also removes queries if they match the queryterm exactly, and strips the
    queryterm from the beginning of the result.
    """
    raw_data = request_data.json()
    suggestions = [
        suggestion.lower().replace(queryterm.lower(), '').strip()
        for suggestion in raw_data[1]
        if suggestion.lower().strip() != queryterm.lower().strip()
    ]
    return suggestions

def store_in_db(connection, suggestions, queryterm, lang, raw_data):
    """
    Stores the data into the database
    """

    sql_suggestions = """
    INSERT INTO `suggestions_bing`
        (`queryterm`, `date`, `lang`, `raw_data`)
    VALUES
        (%s, %s, %s, %s);"""

    sql_terms = """
    INSERT INTO `terms_bing`
        (`suggest_id`, `suggestterm`, `position`, `score`)
    VALUES
        (%s, %s, %s, %s);"""

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql_suggestions,
                           (queryterm, datetime.datetime.now(), lang, raw_data.content))
            suggest_id = cursor.lastrowid
            for position, suggestterm in enumerate(suggestions):
                cursor.execute(sql_terms,
                               (suggest_id, suggestterm, position, 0))
    except:
        log_error("Unexpected database error: Could not write results to database")
        raise

def do_request(lang, queryterm, connection):
    """
    Iterates through each URL, performing an autocomplete API lookup on each
    using the parameters
    """
    counter = 0
    try:
        request_data = query_bing_suggest(query=queryterm, lang=lang)
        suggestions = get_suggestion_terms(request_data=request_data, queryterm=queryterm)
        LOG.debug(suggestions)
        LOG.info('Thread: %s query: %s\tlang: %s', threading.get_ident(), queryterm, lang)
        store_in_db(connection=connection, suggestions=suggestions, queryterm=queryterm,
                    lang=lang, raw_data=request_data)
        counter = counter + 1
    except:
        print("Unexpected error:", sys.exc_info())
        log_error(repr(sys.exc_info()))
        log_error(repr(request_data.content))
    return counter

def do_languages(queryterm, inputfile):
    """
    Iterates through each language, calling do_request() on each
    """
    counter = 0
    connection = db_connect()
    for lang in LANGUAGES:
        if ('turks.csv' in inputfile and lang == 'tr') or (lang != 'tr'):
            counter = counter + do_request(lang=lang, queryterm=queryterm,
                                           connection=connection)
            #sleep(random.randint(0, 1)) # sleep between 1 and 2 seconds between each 2 queries
    connection.commit()
    connection.close()
    return counter

def do_queryterms(queryterms, inputfile):
    """
    Calls do_languages for each queryterm and runs it in its own thread.
    """
    return execute_in_thread_pool(do_languages, queryterms, inputfile)

def main():
    """
    Main function
    """
    inputfile = ''
    args = parse_args()
    queryterms = read_csv(args.inputfile)
    start = timer()
    counter = do_queryterms(queryterms=queryterms, inputfile=inputfile)
    LOG.info('Done after %s seconds. In total we wrote %s results into the database',
             make_timestamp(start), counter)

if __name__ == "__main__":
    main()
