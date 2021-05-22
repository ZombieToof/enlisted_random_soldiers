from datetime import datetime
from pprint import pprint

import logging
import os


LOG_LEVEL = logging.WARNING
LOG_LEVEL = logging.DEBUG


log = logging.getLogger(__file__)
log.setLevel(LOG_LEVEL)


BY_ITEM = "by_item"
BY_COUNT = "by_count"
BY_LEVEL = "by_level"
POOL_ITEMS = "pool_items"
TOTAL_RECEIVED = "total_drops"
TOTAL_BUYS = "total_buys"

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
    "sy": "Sniper III",
    "ta": "Tanker",
    "tt": "Tanker II",
    "tr": "Trooper",
    "tx": "Trooper II",
}

WEAPONS = {
    "fw35": "Flammenwerfer 35",
    "gw36": "Granatwerfer 36",
    "mg42": "MG 42",
    "br30": "Breda Mod. 30",
    "mg34": "MG 34",
    "fg42": "FG 42",
    "gw43": "Gewehr 43",
    "mp35": "MP 35/I",
    "be18": "Beretta M1918",
    "fn43": "FNAB-43",
    "mp34": "MP 38(o)",
    "mp40": "MP 40",
    "k98k": "Kar98k",
    "k98l": "Kar98k with Schiessbecher grenade launcher",
    "mann": "Mannlicher M1895",
    "ma36": "MAS-36",
    "fg4x": "FG 42 II",
    "sg43": "Sniper Gewehr 43",
    "k98s": "Kar98k with scope mount",
    "stpi": "Sturmpistole",
    "z383": "ZK-383",
    "wp38": "Walther P38",
    "p08l": "P08 Luger",
    "wapp": "Walther PP",
    "atxx": "Axe",
}

IGNORE = object()

WEAPON_LEVEL_CORRECTIONS = {
    "fw35": IGNORE,
    "gw36": IGNORE,
    "mg42": 2,
    "br30": 1,
    "mg34": 1,
    "fg42": 2,
    "mp35": 2,
    "be18": 1,
    "k98l": 1,
    "fg4x": 2,
    "sg43": 1,
    "stpi": IGNORE,
    "z383": 2,
    "wp38": IGNORE,
    "p08l": IGNORE,
    "wapp": IGNORE,
    "atxx": IGNORE,
}

PISTOLS = ["wp38", "p08l", "wapp"]
null_marker = object()


def setup_pool(line, pools, all_items):
    if line in pools:
        raise AssertionError("Pool %s exists already")

    pool = {"name": line}

    # setup pool data skeleton
    pool_items = line.split(':')[1].strip()
    pool_items = [item for item in pool_items.split()]
    pool[POOL_ITEMS] = pool_items
    pool[TOTAL_RECEIVED] = 0
    pool[TOTAL_BUYS] = 0

    # assure our pool description is consitent
    missing = [item for item in pool_items if item not in all_items.keys()]
    if missing:
        print("Pool item missmatch.")
        pprint(pool_items)
        pprint(all_items.keys())

    # initialize data structure
    for (key, entries) in [
        [BY_ITEM, pool_items],
        [BY_LEVEL, range(1, 6)],
        [BY_COUNT, range(1, 4)],
    ]:
        pool[key] = dict([(entry, 0) for entry in entries])

    pools[line] = pool
    return pool

def add_to_pool(line, pool, level_corrections):
    log.debug("Processing %s" % line)

    # ignore dates
    line = line.strip()
    date = None
    try:
        date = datetime.strptime(line, "%Y-%m-%d")
        return
    except ValueError:
        pass

    received_items = line.split()
    pool[BY_COUNT][len(received_items)] += 1
    pool[TOTAL_BUYS] += 1
    for item in received_items:
        item_class = item[0:-1]
        pool[BY_ITEM][item_class] += 1
        item_level = int(item[-1])
        level_correction = level_corrections.get(item_class, 0)

        # Ignore anything that can't be leveled and correct the level so we only
        # record the 4 effective levels of a weapon (base + 3 upgrades)
        if level_correction is IGNORE:
            continue
        item_level = item_level - level_correction
        pool[BY_LEVEL][item_level] += 1


def print_h1(h1, char="-"):
    print(h1)
    print(len(h1) * char)


def print_pool(pool, all_items):
    print_h1(pool["name"])
    buys = pool[TOTAL_BUYS]
    received = pool[TOTAL_RECEIVED]
    print("Buys: %s" % buys)
    print("Items received: %s" % received)
    print("Average number of items per buy: %.2f" % (float(received) / float(buys)))

    # print counts
    print_subdict(pool[BY_ITEM], "By item", title_resolver=lambda x: all_items[x])
    print_subdict(pool[BY_LEVEL], "By level", print_average=True)
    print_subdict(
        pool[BY_COUNT], "By number of items received per buy", print_average=True
    )
    print()


def print_value(title, value):
    print("%s: %s" % (title, value))


def print_subdict(subdict, title, title_resolver=lambda x: x, print_average=False):
    print(title)
    total_count = float(sum(subdict.values()))
    for key in sorted(subdict.keys()):
        value = subdict[key]
        print(
            "  %s: %s (%.2f%%)"
            % (title_resolver(key), value, (float(value) / total_count * 100.0))
        )
    if print_average:
        average = (
            sum([float(key * value) for (key, value) in subdict.items()])
        ) / total_count
        print("  Average: %.2f" % average)


def print_levels_by_patch(pools):
    print()
    print_h1("By Level - prepatch/postpatch")
    for substring in ["prepatch", "postpatch", "All"]:
        collected = {}
        total_buys = 0
        for pool in pools:
            if substring == "All":
               pass
            elif substring not in pool["name"]:
                continue
            for level, count in pool[BY_LEVEL].items():
                collected[level] = collected.get(level, 0) + count
            total_buys += pool[TOTAL_BUYS]

        if total_buys == 0:
            continue
        total_items = sum(collected.values())
        print_subdict(collected, substring, print_average=True)
        print("  Total buys: %s" % total_buys)
        print("  Average items per buy: %.2f" % (total_items / total_buys))


def print_pistol_averages(pools):
    """
    calculate average drop rate of pistols. This assumes that the drop
    rate does not depend on the size of the pool of weapons.
    """
    total_buys = 0
    pistol_drops = 0
    for pool in pools:
        total_buys += pool[TOTAL_BUYS]
        for code, count in pool[BY_ITEM].items():
            if code in PISTOLS:
                pistol_drops += count
    print("\n")
    print_h1("Pistols")
    print("  Total buys: %s" % total_buys)
    print("  Pistols dropped: %s" % pistol_drops)
    print("  Average: %.2f" % ((pistol_drops / total_buys) * 100))
    

def get_data_file_path(filename):
    return os.path.join(os.path.dirname(__file__), 'data', filename)


def analyse():
    pairs = [["soldiers.txt", CLASSES, "Soldiers", {}, False],
             ["weapons.txt", WEAPONS, "Weapons", WEAPON_LEVEL_CORRECTIONS, True],
             ]
    for (filename, items, title, level_corretions, analyse_pistols) in pairs:
        analyse_file(filename, items, title, level_corretions, analyse_pistols)


def analyse_file(filename, items, title, level_corrections, analyse_pistols):
    pools = {}
    pool = None
    with open(get_data_file_path(filename), "r") as infile:
        for line in infile:
            line = line.strip()
            if not line or line.startswith("Campaign"):
                continue
            if line.startswith("Pool"):
                pool = setup_pool(line, pools, items)
                continue
            try:
                add_to_pool(line, pool, level_corrections)
            except:
                pprint("An error occured with the following pool and line")
                pprint(pools)
                pprint(line)
                raise

    print_h1(title, char="=")
    for pool in pools.values():
        print_pool(pool, items)

    print_levels_by_patch(pools.values())
    if analyse_pistols:
        print_pistol_averages(pools.values())

if __name__ == "__main__":
    analyse()
