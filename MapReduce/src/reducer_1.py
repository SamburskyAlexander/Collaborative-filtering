#! /usr/bin/python3

import sys

user = None
current_user = None
current_count = 0
current_ratings = 0

for line in sys.stdin:
	line = line.strip()
	user, rating = line.split('\t', 1)
	try:
		rating = float(rating)
	except ValueError:
		continue
	if current_user == user:
		current_ratings += rating
		current_count += 1
	else:
		if current_ratings:
			print('%s\t%s' % (current_user, current_ratings / current_count))
		current_ratings = rating
		current_count = 1
		current_user = user

print('%s\t%s' % (current_user, current_ratings / current_count))
