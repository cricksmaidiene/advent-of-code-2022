with open("input.txt") as f:
    inp_tup: list[tuple[str, str]] = [
        tuple(x.replace("\n", "").split(",")) for x in f.readlines()
    ]

"""
Part 1
"""

# create an array for marking 1 or 0 for fully subseted section
mark_subsets: list[int] = []

# for each pair of sections given
for x in inp_tup:
    elf_pair: list[set[int]] = []
    # for each section of the pair of sections
    for y in x:
        range_split: list[str] = y.split("-")
        start, end = int(range_split[0]), int(range_split[1])
        # convert string to an integer range and make a set out of it
        elf_pair.append(set([z for z in range(start, end + 1)]))

    # extract sets from list elements
    set_1, set_2 = elf_pair[0], elf_pair[1]
    # find complete subsets and mark the section as a subset
    if set_1.issubset(set_2) or set_2.issubset(set_1):
        mark_subsets.append(1)
    else:
        mark_subsets.append(0)


print(sum(mark_subsets))

"""
Part 2
"""

mark_overlaps: list[int] = []
# same logic for loop as before except overlap check
for x in inp_tup:
    elf_pair: list[set[int]] = []
    for y in x:
        range_split: list[str] = y.split("-")
        start, end = int(range_split[0]), int(range_split[1])
        elf_pair.append(set([z for z in range(start, end + 1)]))

    set_1, set_2 = elf_pair[0], elf_pair[1]
    # check intersection instead of overlap
    if set_1.intersection(set_2):
        mark_overlaps.append(1)
    else:
        mark_overlaps.append(0)

print(sum(mark_overlaps))
