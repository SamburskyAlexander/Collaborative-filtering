#!/usr/bin/python3

import sys

user = None
current_user = None
current_items = []

for line in sys.stdin:
    line = line.strip()
    user, movie_info = line.split('\t', 1)
    movie_info = movie_info.split(' ')
    movie = movie_info[0]
    bias = movie_info[1]
    
    if current_user == user:
        current_items += [(movie, bias)]
    else:
        if len(current_items) >= 1:
            for i in range(len(current_items)):
                for j in range(i):
                    print('%s %s\t%s %s' % (current_items[j][0], current_items[i][0], current_items[j][1], current_items[i][1]))
        current_items = [(movie, bias)]
        current_user = user

for i in range(len(current_items)):
    for j in range(i):
        print('%s %s\t%s %s' % (current_items[j][0], current_items[i][0], current_items[j][1], current_items[i][1]))
