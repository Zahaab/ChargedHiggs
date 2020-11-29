import sys
import os
import math

events = [8530000, 9110000, 47710000, 39570000, 2560000,
          40000, 40000, 40000, 3090000, 2290000, 22130000]

temp = []

bins = []

for i in sorted(events):
    temp.append(i)
    if sum(temp) >= sum(events)/5:
        bins.append(temp)
        temp = []

print(bins)

for i in bins:
    print(sum(i))
