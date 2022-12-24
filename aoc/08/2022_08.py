with open("input.txt") as f:
    inp: str = f.readlines()
    inp_tup = [x.replace("\n", "") for x in inp]

# verify if the input is a square
len(inp_tup[0]) == len(inp_tup)


def get_all_cardinal_neighbours(row_indx: int, col_indx: int) -> dict[str, list[int]]:
    """Given a row and column index, return a dictionary of all cardinal neighbours
    across the entire row and column that the index belongs to. The cardinal neighbours
    are returned in the order of north, east, west, south. The cardinal neighbours are
    returned as a list of integers and ordered by their distance from the index.

    Requires `inp_tup` global variable to be defined.

    Args:
        row_indx (int): The row index of the cell to get the cardinal neighbours of.
        col_indx (int): The column index of the cell to get the cardinal neighbours of.

    Returns:
        dict[str, list[int]]: A dictionary of cardinal neighbours with the cardinal direction as the key and a list of integers as the value.
    """
    return dict(
        north=list(reversed([int(x[col_indx]) for x in inp_tup[0:row_indx]])),
        east=[int(x) for x in inp_tup[row_indx][col_indx + 1 :]],
        west=list(reversed([int(x) for x in inp_tup[row_indx][:col_indx]])),
        south=[int(x[col_indx]) for x in inp_tup[row_indx + 1 :]],
    )


"""
Part 1
"""

num_visible: int = 0

for row_indx, tree_row in enumerate(inp_tup):
    if row_indx in (0, len(inp_tup) - 1):
        num_visible += len(tree_row)
        continue

    for col_indx, tree_height in enumerate(tree_row):
        if col_indx in (0, len(tree_row) - 1):
            num_visible += 1
            continue

        tree_height_int: int = int(tree_height)

        if not tree_height_int:
            continue

        cardinal_neighbours: dict[str, list[int]] = get_all_cardinal_neighbours(
            row_indx, col_indx
        )

        cardinal_visible_bitmap: list[int | None] = []

        for cardinal_direction, cardinal_trees in cardinal_neighbours.items():
            cardinal_visible: bool = True
            for candidate_tree_height in cardinal_trees:
                if candidate_tree_height >= tree_height_int:
                    cardinal_visible = False
                    break

            cardinal_visible_bitmap.append(
                1
            ) if cardinal_visible else cardinal_visible_bitmap.append(0)

        if any(cardinal_visible_bitmap):
            num_visible += 1

print(f"Part 1: {num_visible}")

"""
Part 2
"""

max_scenic_score: int = 0

for row_indx, tree_row in enumerate(inp_tup):
    for col_indx, tree_height in enumerate(tree_row):
        cardinal_neighbours: dict[str, list[int]] = get_all_cardinal_neighbours(
            row_indx, col_indx
        )
        tree_height_int: int = int(tree_height)

        scenic_score: int = 1
        for cardinal_direction, cardinal_trees in cardinal_neighbours.items():
            cardinal_tree_count: int = 0

            for candidate_tree_height in cardinal_trees:
                cardinal_tree_count += 1

                if candidate_tree_height >= tree_height_int:
                    break

            scenic_score *= cardinal_tree_count

        if scenic_score > max_scenic_score:
            max_scenic_score = scenic_score

print(f"Part 2: {max_scenic_score}")
