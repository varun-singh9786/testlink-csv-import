import sys

import csv


def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]


def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')

if len(sys.argv) == 1:
    print "Please input CSV file path."
    sys.exit(1)
file_path = sys.argv[1]
with open(file_path) as f:
    lines = unicode_csv_reader(f)
    for l in lines:
        print l
