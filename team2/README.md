# Poker-Dice Battler

> Epitech JAM — thème : **Le Hasard**

Survive as many levels as possible. Each level you face a 300-HP boss — kill it and the next one hits harder. Your score is the number of levels cleared.

## Requirements

```bash
pip install pillow
# Dice Quest (linked group's game) also needs:
pip install pygame
```

## Run

```bash
python main.py
```

Must be run from the project root (asset paths are relative).

## How to play

Each turn:
1. **Roll** 5 dice — you get up to 3 rerolls
2. **Hold** any dice before rerolling by clicking them (gold border = held)
3. Choose **Attack** (deal score as damage) or **Heal** (restore HP, excess becomes Armor)
4. The boss counter-attacks — then the next turn begins

### Scoring

`Score = (Base chips + Sum of all 5 dice) × Multiplier`

| Hand | Chips | Multi |
|---|---|---|
| Five of a Kind | 120 | ×12 |
| Four of a Kind | 60 | ×7 |
| Straight | 50 | ×5 |
| Full House | 40 | ×4 |
| Three of a Kind | 30 | ×3 |
| Two Pair | 20 | ×2 |
| Pair | 10 | ×2 |
| High Card | 5 | ×1 |

The active hand is highlighted in the combo table on the bottom-right of the screen.

### Boss

The boss has **300 HP** and deals fixed damage per turn — doubling every level:

| Level | Boss damage/turn |
|---|---|
| 1 | 5 |
| 2 | 10 |
| 3 | 20 |
| 4 | 40 |
| … | … |

Kill the boss → next level, boss HP resets to 300, damage doubles.

### Overheal

Healing beyond max HP converts the surplus into **Armor**, which absorbs the next boss hits first.

## Dice Quest

**DICE QUEST ↗** in the main menu launches [Dice Quest](https://github.com/Felix-Lcr/random_hackaton), our linked group's game, in a separate window.

To get the submodule after cloning:

```bash
git submodule update --init
```
