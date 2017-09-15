#!/usr/bin/env python2

import fileinput
import math
import sys


def calculate_entropy(data):
    counts = {}
    for value in data:
        if value not in counts:
            counts[value] = 1
        else:
            counts[value] += 1

    entropy = float(0)
    for value, count in counts.items():
        entropy -= (float(count) / len(data)) * math.log(float(count) / len(data))

    return entropy


def replace_values_with_deltas(data, range):
    new_data = []
    for i, item in enumerate(data):
        new_data.append((data[i] - data[i - 1]) % range)
    return new_data


content = []
if len(sys.argv) >= 2:
    files = sys.argv[1]
else:
    files = None
for line in fileinput.input(files=files):
    stripped_line = line.strip()
    if stripped_line:
        content.append(int(stripped_line))

if len(sys.argv) >= 4:
    lower = min(int(sys.argv[2]), min(content))
    upper = max(int(sys.argv[3]), max(content))
    total_range = upper - lower + 1
else:
    print "No range provided.  Not counting any values with frequency of 0."
    total_range = max(content) - min(content) + 1
print "Using total range of %d." % total_range

print

max_possible_entropy = math.log(total_range)
print "max_possible_entropy =", max_possible_entropy

print

overall_entropy = calculate_entropy(content)
print "overall_entropy =", overall_entropy
if overall_entropy == 0:
    overall_randomness = 0
else:
    overall_randomness = overall_entropy / max_possible_entropy
print "overall_randomness =", overall_randomness

print

differential_content = replace_values_with_deltas(content, total_range)
differential_entropy = calculate_entropy(differential_content)
print "differential_entropy =", differential_entropy
if differential_entropy == 0:
    differential_randomness = 0
else:
    differential_randomness = differential_entropy / max_possible_entropy
print "differential_randomness =", differential_randomness

print

estimated_randomness = min(overall_randomness, differential_randomness)
print "estimated_randomness =", estimated_randomness
