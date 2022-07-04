#! /usr/bin/python3

import sys

user = None
current_user = None
top_k = 1

for line in sys.stdin:
	line = line.strip()
	user_rating_movie = line.split('\t')[0]
	user, rating, movie = user_rating_movie.split('_', 2)
	rating = float(rating)
	if current_user == user:
		print("@%f#%s" % (5.0-rating, movie), end='')
		top_k += 1
	else:
		top_k = 1
		print('\n')
		print("%s@%f#%s" % (user, 5.0-rating, movie), end='')
		current_user = user
		top_k += 1
