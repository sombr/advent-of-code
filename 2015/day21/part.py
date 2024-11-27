#!/usr/bin/python3

import numpy as np

def check_if_player_wins(stats):
    cost, dmg, arm = stats
    health = 100

    enemy_dmg = 8
    enemy_arm = 2
    enemy_health = 100

    player_impact = max(1, dmg - enemy_arm)
    enemy_impact = max(1, enemy_dmg - arm)

    player_steps = np.round(enemy_health / player_impact)
    enemy_steps = np.round(health / enemy_impact)

    return player_impact >= enemy_impact

def main():
    weapons = np.array([
        [ 8, 4, 0],
        [10, 5, 0],
        [25, 6, 0],
        [40, 7, 0],
        [74, 8, 0]
    ], dtype=np.int32)

    armor = np.array([
        [  0, 0, 0],
        [ 13, 0, 1],
        [ 31, 0, 2],
        [ 53, 0, 3],
        [ 75, 0, 4],
        [102, 0, 5]
    ])

    rings = np.array([
        [  0, 0, 0],
        [ 25, 1, 0],
        [ 50, 2, 0],
        [100, 3, 0],
        [ 20, 0, 1],
        [ 40, 0, 2],
        [ 80, 0, 3]
    ])

    # just brute force this
    cost = np.inf
    cost2 = 0
    for w in range(weapons.shape[0]):
        for a in range(armor.shape[0]):
            for r1 in range(rings.shape[0]):
                for r2 in range(rings.shape[0]):
                    if r1 == r2 and r1 > 0:
                        continue
                    stats = weapons[w] + armor[a] + rings[r1] + rings[r2]
                    if check_if_player_wins(stats):
                        cost = min(cost, stats[0])
                    if not check_if_player_wins(stats):
                        cost2 = max(cost2, stats[0])
    
    print(f">>>part1 min cost: {cost}")
    print(f">>>part2 max cost: {cost2}")

main()