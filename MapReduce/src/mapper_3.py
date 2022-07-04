#!/usr/bin/python3

import sys

for line in sys.stdin:
	line = line.strip()
	line = line.split('\t')
	i, j = line[0].split(' ')
	dr_i, dr_j = line[1].split(' ')
	if int(j) > int(i):
		print('%s %s\t%s %s' % (i, j, dr_i, dr_j))
	else:
		print('%s %s\t%s %s' % (j, i, dr_j, dr_i))
    
