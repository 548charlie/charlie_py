#!/usr/bin/env python

import os
import sys

if len(sys.argv) != 3:
    print "Uages: %s <file_1> <file2>\n" %(sys.argv[0])
    sys.exit(0)

test_file = sys.argv[1]
prod_file = sys.argv[2]
test_data = {}
prod_data = {}
common_data = {}

fh = open(test_file, 'r')
for line in fh.readlines():
    line = line.strip()
    words = line.split(',')
    key = words[1].strip()
    if test_data.has_key(key) == False:
        test_data[key] = line
fh.close()

fh = open(prod_file, 'r')
for line in fh.readlines():
    line = line.strip()
    words = line.split(',')

    key = words[1].strip()
    if prod_data.has_key(key) == False:
        prod_data[key] = line

fh.close()

for key in test_data.keys():
    if common_data.has_key(key) == False:
            if prod_data.has_key(key) == True:
                site, thread = prod_data[key].split(',')
                common_data[key] = test_data[key] + "," + thread
            else :
                common_data[key] = test_data[key]

for key in prod_data.keys():
    if common_data.has_key(key) == False:
        line = prod_data[key]
        site, thread = line.split(',')
        common_data[key] =site + ",,," + thread
        
fh = open("common_threads.csv", "w")
for key in common_data.keys():
     print "%s and data %s" %(key, common_data[key])
     fh.write(common_data[key] + "\n")
fh.close()
