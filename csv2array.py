#!/usr/local/bin/python2.7

import argparse
import csv

parser = argparse.ArgumentParser(description='convert CSV file to C array')
parser.add_argument('ifile', type=argparse.FileType('r'), default='-')
parser.add_argument('-w', dest='width', type=int, default=0)
parser.add_argument('-o', dest='ofile', type=argparse.FileType('w'), default='-')
parser.add_argument('-d', dest='delimiter', default=',')
args = parser.parse_args()

ifilereader = csv.reader(args.ifile, delimiter=args.delimiter)
data = []
for row in ifilereader:
    if len(row) == 1:           # only one column of data
        data.append(row[0])
    else:                       # multiple columns of data
        data.append(row)
        
if len(data) == 1:              # only one line of data
    data = data[0]


def format_row(row):
    formatted_elements = [str.rjust(element, args.width) for element in row];
    return str.join(', ', formatted_elements)
     
if type(data[0]) is list:       # 2D array
    args.ofile.write('{\n')
    for row in data:
        args.ofile.write('\t{ ' + format_row(row) + ' },\n')
    args.ofile.write('};\n')
else:                           # 1D array
    args.ofile.write('{ ' + format_row(data) + ' };\n')

args.ifile.close()
args.ofile.close()


