'''
To see how much margin of error you have, determine the number of ways you can beat the record in each race; in this example, if you multiply these values together, you get 288 (4 * 8 * 9).

Determine the number of ways you could beat the record in each race. What do you get if you multiply these numbers together?
'''

with open("input") as f:
    lines = f.read().splitlines()

# Time:      7  15   30
# Distance:  9  40  200

times = map(int, lines[0].split("Time:")[1].strip().split())
distances = map(int, lines[1].split("Distance:")[1].strip().split())

records = zip(times, distances)
# ('7', '9'), ('15', '40'), ('30', '200')]

# part 2

times = int(lines[0].split("Time:")[1].replace(" ", ""))
distances = int(lines[1].split("Distance:")[1].replace(" ", ""))
records = [(times, distances)]

number_of_ways_to_beat_the_records = []
''' brute force
for time, record_distance in list(records):
    record_ways = 0
    print()
    for pushtime in range(time+1):
        traveltime = time-pushtime
        distance = traveltime * pushtime
        record = ""
        if distance > record_distance:
            record = "(record)" 
            record_ways += 1
        print(f"D = {traveltime} * {pushtime} = {distance} {record}")
    number_of_ways_to_beat_the_records.append(record_ways)

from numpy import prod 
print(prod(number_of_ways_to_beat_the_records))
'''

# Part 2: stop when first record found and do some math with the index.

not_a_record = 0
for time, record_distance in list(records):
    for pushtime in range(time+1):
        traveltime = time-pushtime
        distance = traveltime * pushtime
        if distance > record_distance:
            print(f"{traveltime} * {pushtime} > {record_distance}")
            break
        not_a_record += 1

print()
print(f"{records[0][0] - (2 * not_a_record - 1)} ways to beat the record")

