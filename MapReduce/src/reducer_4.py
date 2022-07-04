#!/usr/bin/python3

import sys

ui = None
current_ui = None
num = 0.0
denom = 0.0

current_ratings = dict()
current_sims = dict()

for line in sys.stdin:
	line = line.strip()
	ui, second_part = line.split('\t', 1)
	second_part = second_part.split(' ')
	
	try:
		if current_ui == ui:
			if second_part[0] == 'r':
				movie = second_part[1]
				rating = second_part[2]
				current_ratings[int(movie)] = float(rating)
			else:
				movie = second_part[1]
				sim = second_part[2]
				current_sims[int(movie)] = float(sim)
		else:
			if not current_ui is None:
				for m in current_ratings:
					try:
						num += current_sims[m] * current_ratings[m]
						denom += current_sims[m]
					except:
						continue
				if denom == 0:
					res_rating = 0.0
				else:
					res_rating = num / denom
				print("%s\t%f" % (current_ui, res_rating))
			current_ui = ui
			num = 0.0
			denom = 0.0
			current_ratings = dict()
			current_sims = dict()
			if second_part[0] == 'r':
				movie = second_part[1]
				rating = second_part[2]
				current_ratings[int(movie)] = float(rating)
			else:
				movie = second_part[1]
				sim = second_part[2]
				current_sims[int(movie)] = float(sim)
	except:
		continue

for m in current_ratings:
	try:
		num += current_sims[m] * current_ratings[m]
		denom += current_sims[m]
	except:
		continue
if denom == 0:
	res_rating = 0.0
else:
	res_rating = num / denom
print("%s\t%f" % (current_ui, res_rating))

