#!/usr/local/bin/python2.7

import argparse
import csv

parser = argparse.ArgumentParser(description='convert CSV file to C array')
parser.add_argument('ifile', type=argparse.FileType('r'), default='-')
parser.add_argument('-w', dest='width', type=int, default=0)
parser.add_argument('-o', dest='ofile', type=argparse.FileType('w'), default='-')
parser.add_argument('-d', dest='delimiter', default=',')
parser.add_argument('-m', dest='macro', action='store_true')

args = parser.parse_args()

if args.macro:
    eol_line = ' \\\n'
    eol_final = '\n'
else:
    eol_line = '\n'
    eol_final = ';\n'
    
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
    args.ofile.write('{' + eol_line)
    for row in data[:-1]:
        args.ofile.write('\t{ ' + format_row(row) + ' },' + eol_line)
    args.ofile.write('\t{ ' + format_row(data[-1]) + ' }' + eol_line)
    args.ofile.write('}' + eol_final)
else:                           # 1D array
    args.ofile.write('{ ' + format_row(data) + ' }' + eol_final)

args.ifile.close()
args.ofile.close()


