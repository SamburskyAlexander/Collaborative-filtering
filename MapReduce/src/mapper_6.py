#! /usr/bin/python3

import sys

def read_file(file_path):
	films = dict()
	for line in open(file_path):
		line = line.split(',')
		try:
			movie = int(line[0])
			name = ""
			for k in line[1:-1]:
				name += k
		except ValueError:
			continue
		
		films[movie] = name
	return films

films = read_file('./movies.csv')

for line in sys.stdin:
	line = line.strip()
	line = line.split('\t')
	user = line[0]
	movie, rating = line[1].split(' ')
	movie = int(movie)
	rating = float(rating)
	movie_name = films[movie]
	print('%s_%f_%s\t1' % (user, 5.0-rating, movie_name))
