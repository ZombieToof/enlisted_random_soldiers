# Enlisted random soldiers (and weapons)

Analyze drop rates for random troop reinforcements (by class, level and number of soldiers) and random weapon deliveries (weapon, normalized level and percent of pistol drops)in Enlisted. This is written to minimize the amount of input and the complexity of the script and is not intended to be pretty.

## Installation

This script is written for Python 3.9.5 and should be run with any Python 3 (and probably even Python 2). Call it with

```
# Path/to/python enlisted_random_soldiers.py
```
while in the directory that contains the python file.


## Data Input

The data is collected in `enlisted_random_soldiers.txt` and `enlisted_random_weapons.txt`. It is grouped in Pools that contain the currently available solder classes.

Data is counted after line starting with "Pool". The line has to continue with the class codes for all classes in the pool, e.g. "Pool: as en sn ta". Each following line is 1 purchase and all soldier are written in the form `<class/weapon code><level>` separated by spaces. E.g. `ap2 en1 sn1` for "Attack Pilot II, Engineer1, Sniper1". The list of class codes is:

```
CLASSES = {
    "as": "Assault",
    "at": "Assault II",
    "ap": "Attack Pilot",
    "ax": "Attack Pilot II",
    "bo": "Bomber",
    "en": "Engineer",
    "ex": "Engineer II",
    "fp": "Fighter pilot",
    "fx": "Fighter pilot",
    "fl": "Flametrooper",
    "gu": "Gunner",
    "gx": "Gunner II",
    "mo": "Mortarman",
    "ra": "Radio Operator",
    "sn": "Sniper",
    "sx": "Sniper II",
    "sx": "Sniper II",
    "ta": "Tanker",
    "tt": "Tanker II",
    "tr": "Trooper",
    "tx": "Trooper II",
}
```
If a class code does not exist or is not listed in the "Pool: ..." title the script will throw an error.

## prepatch/postpatch

The script will list an additional by level section if "Pool.." titles contain the words "prepatch" and/or "postpatch". This was used to see differences in drop rates after the change that you earn bronze cards through XP instead of tasks.

## Output

E.g.

```
Pool_postpatch: as ap bo en fp gu ra sn ta tr
=============================================
Buys: 12
Solders received: 0
Average soldiers per buy: 0.00
By class
  Attack Pilot: 0 (0.00%)
  Assault: 2 (7.41%)
  Bomber: 4 (14.81%)
  Engineer: 2 (7.41%)
  Fighter pilot: 2 (7.41%)
  Gunner: 6 (22.22%)
  Radio Operator: 6 (22.22%)
  Sniper: 2 (7.41%)
  Tanker: 0 (0.00%)
  Trooper: 3 (11.11%)
By Level
  1: 17 (62.96%)
  2: 7 (25.93%)
  3: 3 (11.11%)
  4: 0 (0.00%)
  5: 0 (0.00%)
  Average: 1.48
By number of solders received per buy
  1: 2 (16.67%)
  2: 5 (41.67%)
  3: 5 (41.67%)
  Average: 2.25


By Level - prepatch/postpatch
=============================
prepatch
  1: 104 (68.87%)
  2: 30 (19.87%)
  3: 12 (7.95%)
  4: 5 (3.31%)
  5: 0 (0.00%)
  Average: 1.46
  Total buys: 77
  Average solders per buy: 1.96
postpatch
  1: 46 (64.79%)
  2: 17 (23.94%)
  3: 6 (8.45%)
  4: 2 (2.82%)
  5: 0 (0.00%)
  Average: 1.49
  Total buys: 35
  Average solders per buy: 2.03
```

## Changelog:

* Convert data input from cvs to plain text
* Add tracking of random weapon deliveries