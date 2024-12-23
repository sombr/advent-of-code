#!/usr/bin/python3

import sys
import math
from tqdm import tqdm

def backtrack(connections, nodes, mesh, acc, curmax = 0, progress = False):
    if len(nodes) == 0:
        if len(mesh) > 0:
            m = tuple(sorted(mesh))
            acc.add(m)
            return len(m)
        return 0

    if len(mesh) + len(nodes) <= curmax:
        return curmax

    iteration = nodes
    if progress:
        iteration = tqdm(iteration)

    for node in iteration:
        if node in mesh:
            continue
        if progress:
            iteration.set_description(f"processing {node} curmax {curmax}")
        next_nodes = connections[node] & nodes
        mesh.add(node)
        curmax = max(curmax, backtrack(connections, next_nodes, mesh, acc, curmax))
        mesh.remove(node)

    return curmax

def main():
    links = []
    nodes = set()
    with open(sys.argv[1], "r") as file:
        for line in file:
            line = line.strip()
            if line != "":
                f, t = line.split("-")
                links.append( (f, t) )
                nodes.add(f)
                nodes.add(t)

    connections = {}
    for f, t in links:
        connections[f] = connections.get(f, set())
        connections[t] = connections.get(t, set())

        connections[f].add(t)
        connections[t].add(f)

    triplets = set()
    for origin, links in connections.items():
        if origin.startswith("t"):
            for sec in links:
                for third in (connections[sec] & links):
                    triplet = tuple(sorted( [origin, sec, third] ))
                    print(">> ", triplet)
                    triplets.add(triplet)

    print("total >> ", len(triplets))


    acc = set()
    curmax = backtrack(connections, nodes, set(), acc, 0, True)

    largest = max(acc, key=lambda x: len(x))
    print("part2>>")
    print(",".join(largest))

main()
