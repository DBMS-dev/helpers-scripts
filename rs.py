#!/usr/bin/python3
import elasticsearch
import argparse
import csv
from elasticsearch import helpers
import json
from flatten_json import flatten
import sys

'''
Tool for exporting elasticsearch query to CSV file
assumption: the response document is not multidimensional(nested) document.
it will execute elasticsearch query_string,
for example query_string: this AND that OR thus
'''
csv.field_size_limit(sys.maxsize)
parser=argparse.ArgumentParser()
parser.add_argument("-f", "--file", dest="file",
                    help="required: filename", default="rs.csv")

args = vars(parser.parse_args())

file = args['file']
stdoutwriter = csv.writer(sys.stdout,quoting=csv.QUOTE_ALL)
with open(file, 'r', newline='') as f:
    reader = csv.DictReader(f,delimiter=',',quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        dict = json.loads(row['unauthorized_identify.result'])
        company_name = dict.get('company_data').get('name')
        nip = dict.get('company_data').get('ids').get('nip')
        email = None;
        for cd in dict['contact_data']:
            if cd.get('type') == 'email':
                if email is None:
                    email = cd.get('raw')
                elif cd.get('is_main') == True:
                    email = cd.get('raw')

        if email:
            stdoutwriter.writerow([email, company_name, nip])
                
        