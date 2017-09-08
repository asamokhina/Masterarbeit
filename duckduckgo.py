#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crawls the DuckDuckGo API for autocomplete terms
"""

from time import sleep
import csv
import random
import datetime
from timeit import default_timer as timer
import re
import sys
import logging
import argparse
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import pymysql.cursors
import requests
from crawl_utils import *

# global variables
HEADERS = {'User-agent':'Mozilla/5.0'}
URL = 'https://duckduckgo.com/ac/'
MAX_RETRIES = range(5)
TIMEOUT = 1

LOGFILE, LOG = init_logging('crawler_ddg.log')

def log_error(message):
    """
    Outputs a log entry to both the stderr logger and the file logger
    """
    LOG.error(message)
    LOGFILE.error(message)

def query_ddg_suggest(query):
    """
    Sends an HTTP request to the Bing autocomplete API and returns the raw data
    returend by the API.
    """
    params = {'q': query}
    return send_request(LOG, URL, MAX_RETRIES, params, HEADERS, TIMEOUT)

def get_suggestion_terms(request_data, queryterm):
    """
    Parses the raw request_data as JSON and extracts the suggestions.

    Data returned from the DuckDuckGo API is formatted like so:

    [
        {
            "phrase": "angela merkel"
        },
        {
            "phrase": "angela merkel biography"
        }
    ]

    Also removes queries if they match the queryterm exactly, and strips the
    queryterm from the beginning of the result.
    """
    raw_data = request_data.json()
    suggestions = [
        suggestion["phrase"].lower().replace(queryterm.lower(), '').strip()
        for suggestion in raw_data
        if suggestion["phrase"].lower().strip() != queryterm.lower().strip()
    ]
    return suggestions

def store_in_db(connection, suggestions, queryterm, raw_data):
    """
    Stores the data into the database
    """

    sql_suggestions = """
    INSERT INTO `suggestions_ddg`
        (`queryterm`, `date`, `raw_data`)
    VALUES
        (%s, %s, %s);"""

    sql_terms = """
    INSERT INTO `terms_ddg`
        (`suggest_id`, `suggestterm`, `position`, `score`)
    VALUES
        (%s, %s, %s, %s);"""

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql_suggestions,
                           (queryterm, datetime.datetime.now(), raw_data.content))
            suggest_id = cursor.lastrowid
            for position, suggestterm in enumerate(suggestions):
                cursor.execute(sql_terms,
                               (suggest_id, suggestterm, position, 0))
    except:
        log_error("Unexpected database error: Could not write results to database")
        raise

def do_request(queryterm, dummy):
    """
    Iterates through each URL, performing an autocomplete API lookup on each
    using the parameters.
    The dummy arg makes it work with the thread pool abstraction.
    """
    connection = db_connect()
    try:
        request_data = query_ddg_suggest(query=queryterm)
        suggestions = get_suggestion_terms(request_data=request_data, queryterm=queryterm)
        LOG.debug(suggestions)
        LOG.info('Thread: %s query: %s', threading.get_ident(), queryterm)
        store_in_db(connection=connection, suggestions=suggestions, queryterm=queryterm,
                    raw_data=request_data)
    except:
        print("Unexpected error:", sys.exc_info())
        log_error(repr(sys.exc_info()))
        log_error(repr(request_data.content))
    connection.commit()
    connection.close()
    return 1

def do_queryterms(queryterms):
    """
    Calls do_request for each queryterm and runs it in its own thread.
    """
    return execute_in_thread_pool(do_request, queryterms, None)

def main():
    """
    Main function
    """
    inputfile = ''
    args = parse_args()
    queryterms = read_csv(args.inputfile)
    start = timer()
    counter = do_queryterms(queryterms=queryterms)
    LOG.info('Done after %s seconds. In total we wrote %s results into the database',
             make_timestamp(start), counter)

if __name__ == "__main__":
    main()
