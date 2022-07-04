#! /usr/bin/python3

import sys

user = None
current_user = None
top_k = 1

for line in sys.stdin:
	line = line.strip()
	user_rating, movie = line.split('\t')
	user, rating = user_rating.split('_')
	rating = float(rating)
	if current_user == user:
		if top_k <= 100:
			print("%s\t%s %f" % (current_user, movie, 5.0-rating))
			top_k += 1
	else:
		top_k = 1
		print("%s\t%s %f" % (user, movie, 5.0-rating))
		current_user = user
		top_k += 1
