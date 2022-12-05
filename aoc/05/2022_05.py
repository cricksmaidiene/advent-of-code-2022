import re
from itertools import groupby

with open("input.txt") as f:
    inp_tup: list[tuple[str, str]] = [x.replace("\n", "") for x in f.readlines()]

"""
Part 1
"""

# separate crates and moves based on the blank newline in between
crates, moves = [list(g) for k, g in groupby(inp_tup, key=lambda s: s != "") if k]

container_matrix: list[list[str | None]] = []

for each_row in crates:
    # go row by row and add str text as list elements
    spaces_count: int = 0
    row_containers: list[str | None] = []

    # when using split by whitespace, every 3 or so whitespace characters are equivalent to a single "null" container
    for char in each_row.split(" "):
        # add on to spaces count to find multiple of 3 whitepaces
        if char == "":
            spaces_count += 1
            continue

        # find actual spaces / lack of containers between those present
        actual_spaces: int = int(spaces_count / 3)

        # create a list of empty containers between two existing containers
        empty_containers: list[None] = [None for _ in range(actual_spaces)]

        # add existing and null containers to matrix
        row_containers.extend(empty_containers)
        row_containers.append(char.replace("[", "").replace("]", ""))

        # reset spaces count for next window
        spaces_count = 0

    # Add the entire container row to the matrix.
    # Empty containers will show up as None (null)
    container_matrix.append(row_containers)

transposed_matrix: list[list[str | None]] = list(map(list, zip(*container_matrix)))
for x in transposed_matrix:
    x.reverse()

container_map_with_nulls: dict[str, list[str | None]] = {
    x[0]: x[1:] for x in transposed_matrix
}

container_map: dict[int, list[str]] = {
    int(k): [elem for elem in v if elem] for k, v in container_map_with_nulls.items()
}

# create a moves index as a 3-tuple of the form (containers, from, to)
moves_indexed: list[tuple[int, int, int]] = [
    tuple([int(y) for y in re.findall(r"\d+", x)]) for x in moves
]

len(moves_indexed) == len(moves)


def apply_changes(moves: tuple[...], retain_order: bool = False):
    # get moves attrs
    num_containers, source, target = moves

    # use the crane
    chosen_row: list[str] = container_map[source]
    # remove the last set of `num_container` elements
    items_from_row: list[str] = chosen_row[-num_containers:]
    # reverse items since it's a stack push
    if not retain_order:
        items_from_row.reverse()

    # extend target row with items from other row
    container_map[target].extend(items_from_row)
    # remove items from the end of the source row
    container_map[source] = container_map[source][:-num_containers]


for each_move in moves_indexed:
    apply_changes(each_move)


"".join(
    [
        container_top[1]
        for container_top in sorted(
            [
                (row_number, stacked_containers[-1])
                for row_number, stacked_containers in container_map.items()
            ],
            key=lambda x: x[0],
        )
    ]
)

"""
Part 2
"""

container_map: dict[int, list[str]] = {
    int(k): [elem for elem in v if elem] for k, v in container_map_with_nulls.items()
}

for each_move in moves_indexed:
    apply_changes(each_move, retain_order=True)

"".join(
    [
        container_top[1]
        for container_top in sorted(
            [
                (row_number, stacked_containers[-1])
                for row_number, stacked_containers in container_map.items()
            ],
            key=lambda x: x[0],
        )
    ]
)
