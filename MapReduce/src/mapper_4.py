#!/usr/bin/python3

import sys

def read_file(file_path):
	all_user_info = dict()
	all_films = set()
	for line in open(file_path):
		line = line.split(',')
		try:
			user = int(line[0])
			movie = int(line[1])
		except ValueError:
			continue
		if user in all_user_info:
			all_user_info[user].add(movie)
		else:
			all_user_info[user] = set()
		all_films.add(movie)
	return all_user_info, all_films

user_seen, films = read_file('./ratings.csv')
for line in sys.stdin:	
	line = line.strip()
	line = line.split('\t')
	if len(line) == 2: # similarity
		i, j = line[0].split(' ')
		i = int(i)
		j = int(j)
		sim = line[1]
		for user in user_seen:
			accept = [i in user_seen[user], j in user_seen[user]]
			if accept[0] ^ accept[1]:
				if accept[0]:
					print('%i %i\ts %i %s' % (user, j, i, sim))
				else:
					print('%i %i\ts %i %s' % (user, i, j, sim))
	else: # ratings.csv
		line = line[0]
		line = line.split(',')
		try:
			user = int(line[0])
			movie = int(line[1])
			rating = float(line[2])
		except:
			continue
		for f in films.difference(user_seen[user]):
			print('%i %i\tr %i %f' % (user, f, movie, rating))
    
