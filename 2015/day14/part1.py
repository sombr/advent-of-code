#!/usr/bin/env python3
import sys
import re

def main():
    ext = re.compile(r"^(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.$")

    speed = []
    with open(sys.argv[1], "r") as file:
        for line in file:
            # Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
            m = ext.match(line)
            if m:
                speed.append( (
                        # how long to fly, speed,             how long to rest, speed
                        ( int(m.group(3)), int(m.group(2)) ), ( int(m.group(4)), 0 )
                    )
                )
    
    end_time = int(sys.argv[2])

    distance = []
    for ((fly_time, fly_speed), (rest_time, rest_speed)) in speed:
        span_time = fly_time + rest_time
        span_dist = fly_time * fly_speed

        full_spans = end_time // span_time
        remainder = end_time % span_time

        dist = full_spans * span_dist

        print(f">>> span time: {span_time} span dist: {span_dist}, full spans: {full_spans}, dist: {dist}")
        print(f">>> remainder: {remainder} fly time:{fly_time}")

        remainder_in_flight = min(remainder, fly_time)
        dist += remainder_in_flight * fly_speed
        
        distance.append(dist)

    print(distance)

    print(f">>> part1 {max(distance)}")

main()