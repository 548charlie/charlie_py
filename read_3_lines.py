#!/usr/bin/env python

import re
import sys
if len(sys.argv) < 2 :
    print "Usage: %s <pattern> "% sys.argv[0]
    sys.exit()
search_for = sys.argv[1]
fh = open("test.txt", "r")
lines = fh.readlines()
count = 0
line_counts = 0
text = ""

pattern = re.compile(search_for, re.IGNORECASE)
for line in lines:
    line = line.strip()
    if count == 0:
        if line == "end_prolog" :
            count = 1
        continue
    if line_counts < 3 :
        text = text + " " +line
        line_counts = line_counts + 1
    if line_counts == 3:
        match = pattern.search(text)
        if match :
            print text
        line_counts = 0
        text = ""
fh.close()
