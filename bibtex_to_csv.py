#!/usr/bin/env python
# Initially written by Heather Piwowar, June 2011
# Public domain: have at it!
# For exporting bibtex info into csv for running stats

import csv
import re
from pybtex.database.input import bibtex as bibtex_in
from pybtex.database import Person
from pybtex.database.output import bibtex as bibtex_out
from operator import itemgetter, attrgetter
from collections import defaultdict
import pprint
import sys

def read_bib(bib_filename):
    parser = bibtex_in.Parser()
    bib_data = parser.parse_file(bib_filename)
    return(bib_data)

def get_all_fieldnames(list_of_entries):
    fieldnames_set = set()
    for entry in list_of_entries:
        fieldnames_set = fieldnames_set.union(set(entry.keys()))
    fieldnames = sorted(list(fieldnames_set))
    return(fieldnames)

def get_encoded_row(row):
    encoded_row = {}
    for k, v in row.items():
        encoded_row[k] = v.encode('utf8')
    return(encoded_row)

def write_csv(bib_data, csv_filename):
    entries = bib_data.entries
    entries_list = []

    for entry in entries:
        raw_row = entries[entry].fields
        persons = entries[entry].persons # get the authors as well
        encoded_row = get_encoded_row(raw_row)

        # put 'author' into the entries_list
        authors = ''
        for key, value in persons.items():
            authors = authors + str(value)
        encoded_row[u'author'] = authors

        entries_list.append(encoded_row)

    fieldnames = get_all_fieldnames(entries_list)
    writer_dictwriter = csv.DictWriter(open(csv_filename, "wb"),
                                        fieldnames=fieldnames)

    # write the header
    writer_dictwriter.writerow(dict((column,column) for column in fieldnames))

    # write the body
    for entry in entries_list:
        writer_dictwriter.writerow(entry)

    return(csv_filename)

def run_export(bib_filename, csv_filename=None):
    if not csv_filename:
        csv_filename = bib_filename.replace(".bib", ".csv")
    bib_data = read_bib(bib_filename)
    write_csv(bib_data, csv_filename)

run_export("tvcg2011bib.txt","tvcg2011.csv")

