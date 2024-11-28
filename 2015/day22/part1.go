package main

import "fmt"

type Player struct {
    Mana int
    Health int
    Armor int
    ShieldTurns int
    RechargeTurns int
}

type Enemy struct {
    Damage int
    Health int
    PoisonTurns int
}

func backtrack(player Player, enemy Enemy, turn int, manaSpent int) (bool, int) {
    if player.RechargeTurns > 0 {
        player.RechargeTurns--
        player.Mana += 101
    }
    if player.ShieldTurns > 0 {
        player.ShieldTurns--
        player.Armor = 7
    } else {
        player.Armor = 0
    }
    if enemy.PoisonTurns > 0 {
        enemy.PoisonTurns--
        enemy.Health -= 3
    }

    if enemy.Health <= 0 {
        return true, manaSpent
    }
    if player.Health <= 0 || player.Mana <= 0 {
        return false, manaSpent
    }

    couldWin := false
    bestMana := 1_000_000
    if turn % 2 == 0 { // player's turn
        // try magic missile
        var newPlayer = player
        var newEnemy = enemy
        newPlayer.Mana -= 53
        newEnemy.Health -= 4

        isWin, manaCost := backtrack(newPlayer, newEnemy, turn+1, manaSpent+53)
        if isWin && bestMana > manaCost {
            bestMana = manaCost
            couldWin = true
        }

        // try drain
        newPlayer = player
        newEnemy = enemy
        newPlayer.Health += 2
        newPlayer.Mana -= 73
        newEnemy.Health -= 2

        isWin, manaCost = backtrack(newPlayer, newEnemy, turn+1, manaSpent+73)
        if isWin && bestMana > manaCost {
            bestMana = manaCost
            couldWin = true
        }

        // try shield
        if player.ShieldTurns == 0 {
            newPlayer = player
            newEnemy = enemy
            newPlayer.Mana -= 113
            newPlayer.ShieldTurns = 6

            isWin, manaCost = backtrack(newPlayer, newEnemy, turn+1, manaSpent+113)
            if isWin && bestMana > manaCost {
                bestMana = manaCost
                couldWin = true
            }
        }

        // try poison
        if enemy.PoisonTurns == 0 {
            newPlayer = player
            newEnemy = enemy
            newPlayer.Mana -= 173
            newEnemy.PoisonTurns = 6

            isWin, manaCost = backtrack(newPlayer, newEnemy, turn+1, manaSpent+173)
            if isWin && bestMana > manaCost {
                bestMana = manaCost
                couldWin = true
            }
        }

        // try recharge
        if player.RechargeTurns == 0 {
            newPlayer = player
            newEnemy = enemy
            newPlayer.Mana -= 229
            newPlayer.RechargeTurns = 5

            isWin, manaCost = backtrack(newPlayer, newEnemy, turn+1, manaSpent+229)
            if isWin && bestMana > manaCost {
                bestMana = manaCost
                couldWin = true
            }
        }

        return couldWin, bestMana
    } else { // enemy's turn
        effectiveDamage := enemy.Damage - player.Armor
        if effectiveDamage < 1 {
            effectiveDamage = 1
        }
        player.Health -= effectiveDamage

        return backtrack(player, enemy, turn+1, manaSpent)
    }
}

func main() {
    player := Player {
        500,
        50,
        0,
        0,
        0,
    }

    // input
    enemy := Enemy {
        10,
        71,
        0,
    }

    couldWin, bestMana := backtrack(player, enemy, 0, 0)
    fmt.Printf(">>> part 1, player could win: %v with best mana: %v\n", couldWin, bestMana)
}
