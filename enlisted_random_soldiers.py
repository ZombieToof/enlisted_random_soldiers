import csv

from pprint import pprint

BY_CLASS = "by_class"
BY_COUNT = "by_count"
BY_LEVEL = "by_level"
POOL_CLASSES = "pool_classes"
TOTAL_RECEIVED = "total_drops"
TOTAL_BUYS = "total_roles"

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

null_marker = object()


def setup_pool(pool):
    # setup pool data skeleton
    pool_classes = [c for c in pool["name"].split() if len(c) == 2]
    pool[POOL_CLASSES] = pool_classes
    pool[TOTAL_RECEIVED] = 0
    pool[TOTAL_BUYS] = 0

    # assure our pool description is consitent
    missing = [pc for pc in pool_classes if pc not in CLASSES.keys()]
    if missing:
        print("Pool classes missmatch.")
        pprint(pool_classes)
        pprint(CLASSES.keys())

    # initialize data structure
    for (key, entries) in [
        [BY_CLASS, pool_classes],
        [BY_LEVEL, range(1, 6)],
        [BY_COUNT, range(1, 4)],
    ]:
        pool[key] = dict([(entry, 0) for entry in entries])

    return


def setup_pools(row, pools):
    colindex = 0
    for coltext in row:
        if coltext.startswith("Pool"):
            pools[colindex] = {"name": coltext}
            setup_pool(pools[colindex])
            colindex += 1


def add_to_pool(coltext, pool):
    print("Processing %s" % coltext)
    received_soldiers = coltext.split()
    pool[BY_COUNT][len(received_soldiers)] += 1
    pool[TOTAL_BUYS] += 1
    for soldier in received_soldiers:
        soldier_class = soldier[0:2]
        pool[BY_CLASS][soldier_class] += 1
        soldier_level = int(soldier[2])
        pool[BY_LEVEL][soldier_level] += 1


def add_to_pools(row, pools):
    colindex = 0
    for coltext in row:
        if coltext:
            add_to_pool(coltext, pools[colindex])
        colindex += 1


def print_h1(h1):
    print(h1)
    print(len(h1) * "=")


def print_pool(pool):
    print_h1(pool["name"])
    buys = pool[TOTAL_BUYS]
    received = pool[TOTAL_RECEIVED]
    print("Buys: %s" % buys)
    print("Solders received: %s" % received)
    print("Average soldiers per buy: %.2f" % (float(received) / float(buys)))

    # print counts
    print_subdict(pool[BY_CLASS], "By class", title_resolver=lambda x: CLASSES[x])
    print_subdict(pool[BY_LEVEL], "By Level", print_average=True)
    print_subdict(
        pool[BY_COUNT], "By number of solders received per buy", print_average=True
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
    for substring in ["prepatch", "postpatch"]:
        collected = {}
        total_buys = 0
        for pool in pools:
            if substring not in pool["name"]:
                continue
            for level, count in pool[BY_LEVEL].items():
                collected[level] = collected.get(level, 0) + count
            total_buys += pool[TOTAL_BUYS]
        total_soldiers = sum(collected.values())
        print_subdict(collected, substring, print_average=True)
        print("  Total buys: %s" % total_buys)
        print("  Average solders per buy: %.2f" % (total_soldiers / total_buys))


def analyse():
    pools = {}
    with open("enlisted_random_soldiers.csv", "r") as infile:
        reader = csv.reader(infile)
        for row in reader:
            if not pools:
                setup_pools(row, pools)
            elif pools:
                try:
                    add_to_pools(row, pools)
                except:
                    pprint(pools)
                    pprint(row)
                    raise

    for pool in pools.values():
        print_pool(pool)

    print_levels_by_patch(pools.values())


if __name__ == "__main__":
    analyse()
