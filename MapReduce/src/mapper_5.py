#! /usr/bin/python3

import sys

for line in sys.stdin:
	line = line.strip()
	ui, rating = line.split('\t')
	rating = float(rating)
	user, movie = ui.split(' ')
	print("%s_%f\t%s" % (user, 5.0-rating, movie))
