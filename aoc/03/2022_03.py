import string

with open("input.txt") as f:
    inp_tup: list[str] = [x.replace("\n", "") for x in f.readlines()]

"""
Part 1
"""

# slice each string of the list by half
inp_tup_split: list[tuple[str, str]] = [
    (x[0 : int(len(x) / 2)], x[int(len(x) / 2) : len(x)]) for x in inp_tup
]

# Convert each half into a set of unique characters
inp_tup_set: list[tuple[set[str], set[str]]] = [
    (set(x[0]), set(x[1])) for x in inp_tup_split
]

# Use set intersection to return the common character
inp_tup_intersection: list[str] = [
    list(x[0].intersection(x[1]))[0] for x in inp_tup_set
]

# create a mapping of characters to numbers
lowercase_map: dict[str, int] = {
    x: indx + 1 for indx, x in enumerate(string.ascii_lowercase)
}
uppercase_map: dict[str, int] = {
    x: indx + 27 for indx, x in enumerate(string.ascii_uppercase)
}
full_map: dict[str, int] = lowercase_map | uppercase_map

# sum the priorities
print(sum([full_map[x] for x in inp_tup_intersection]))

"""
Part 2
"""

# create groupings of 3 across the list of racksacks
grouped_set: list[list[tuple[set[str], set[str]]]] = [
    inp_tup_set[x : x + 3] for x in range(0, len(inp_tup_set), 3)
]

trio_badges: list[str] = []
for x in grouped_set:
    # For each trio grouping
    trio: list[set[str]] = []
    for y in x:
        # for each dual set of a single rackack
        trio.append(y[0].union(y[1]))
    # get badge based on intersection of 3 sets within the trio
    badge: str = list(set.intersection(*list(trio)))[0]
    # append intersecting element (badge) to main list
    trio_badges.append(badge)

# sum the priorities
print(sum([full_map[x] for x in trio_badges]))
