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

    # this really calls for a heapq, but I'll try brute force first
    points = [ 0 for _ in speed ]
    dist = [ 0 for _ in speed ]

    for t in range(end_time):
        for idx in range(len(speed)):
            ((fly_time, fly_speed), (rest_time, rest_speed)) = speed[idx]
            span_time = fly_time + rest_time

            in_span = t % span_time
            if in_span < fly_time:
                dist[idx] += fly_speed

        cur_best = max(dist)
        for idx in range(len(dist)):
            if dist[idx] == cur_best:
                points[idx] += 1
            
    print(points)
    print(f"part2 >>> {max(points)}")

main()