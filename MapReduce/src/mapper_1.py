#! /usr/bin/python3

import sys

# Get current file name
#sys.stderr.write(f'Current input file: {os.environ["mapreduce_map_input_file"]}\n')

for line in sys.stdin:
	line = line.strip()
	line = line.split(',')
	if len(line) >= 3:
		user_id = line[0]
		rating = line[2]
		print('%s\t%s' % (user_id, rating))
