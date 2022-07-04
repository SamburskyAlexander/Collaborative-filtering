#!/usr/bin/python3

import sys

pair = None
current_pair = None
num = 0
denom1 = 0
denom2 = 0

for line in sys.stdin:
    line = line.strip()
    pair, sim_part = line.split('\t', 1)
    sim_part = sim_part.split(' ')
    
    if current_pair == pair:
        num += float(sim_part[0]) * float(sim_part[1])
        denom1 += float(sim_part[0]) ** 2
        denom2 += float(sim_part[1]) ** 2
    else:
        if not current_pair is None:
            if denom1*denom2 == 0:
                print('%s\t%s' % (current_pair, '0.0'))
            else:
                sim = num/(denom1*denom2)**0.5
                if sim < 0:
                    print('%s\t%s' % (current_pair, '0.0'))
                else:
                    print('%s\t%s' % (current_pair, str(sim)))
        num = float(sim_part[0]) * float(sim_part[1])
        denom1 = float(sim_part[0]) ** 2
        denom2 = float(sim_part[1]) ** 2
        current_pair = pair

if not current_pair is None:
    if denom1*denom2 == 0:
        print('%s\t%s' % (pair, '0.0'))
    else:
        sim = num/(denom1*denom2)**0.5
        if sim < 0:
            print('%s\t%s' % (current_pair, '0.0'))
        else:
            print('%s\t%s' % (current_pair, str(sim)))
