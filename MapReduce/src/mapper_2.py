#!/usr/bin/python3

import sys

def read_file(file_path):
	return {line.split('\t')[0]: float(line.split('\t')[1]) for line in open(file_path) if len(line.split('\t'))>=2}
	
users_means = read_file('./mean_ratings.txt')

for line in sys.stdin:
	line = line.strip()
	line = line.split(',')
	
	if len(line) >= 3:
		user_id = line[0]
		movie_id = line[1]
		try:
			rating = float(line[2])	
		except ValueError:
			continue
		print('%s\t%s %s' % (user_id, movie_id, str(rating - users_means[user_id])))
