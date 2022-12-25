with open("input.txt") as f:
    inp: str = f.readlines()
    inp_tup = [x.replace("\n", "") for x in inp]

# verify if the input is a square
assert len(inp_tup[0]) == len(inp_tup)


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
        dict[str, list[int]]: A dictionary of cardinal neighbours with the cardinal
            direction as the key and a list of integers as the value.
    """
    return dict(
        north=list(reversed([int(x[col_indx]) for x in inp_tup[0:row_indx]])),
        east=[int(x) for x in inp_tup[row_indx][col_indx + 1:]],
        west=list(reversed([int(x) for x in inp_tup[row_indx][:col_indx]])),
        south=[int(x[col_indx]) for x in inp_tup[row_indx + 1:]],
    )


"""
Part 1
"""

# total number of visible trees
num_visible: int = 0

for row_indx, tree_row in enumerate(inp_tup):
    if row_indx in (0, len(inp_tup) - 1):
        # if the row is the first or last row, all trees are visible
        num_visible += len(tree_row)
        # no need to check the rest of the trees in this row
        continue

    for col_indx, tree_height in enumerate(tree_row):
        if col_indx in (0, len(tree_row) - 1):
            # if the column is the first or last column, the tree is visible
            num_visible += 1
            continue

        tree_height_int: int = int(tree_height)

        if not tree_height_int:
            # if the tree height is 0, the tree is not visible
            continue

        cardinal_neighbours: dict[str, list[int]] = get_all_cardinal_neighbours(
            row_indx, col_indx
        )

        cardinal_visible_bitmap: list[int | None] = []
        # 1 if visible, 0 if not visible for each cardinal direction

        for cardinal_direction, cardinal_trees in cardinal_neighbours.items():
            # assume visible, and disprove
            cardinal_visible: bool = True
            for candidate_tree_height in cardinal_trees:
                # if a tree is taller than the current tree, the current tree is not visible
                if candidate_tree_height >= tree_height_int:
                    cardinal_visible = False
                    # no need to check the rest of the trees in this cardinal direction
                    break

            # append the visibility of the current cardinal direction to the bitmap
            cardinal_visible_bitmap.append(
                1
            ) if cardinal_visible else cardinal_visible_bitmap.append(0)

        # if any of the cardinal directions are visible, the current tree is visible
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

        # the scenic score is the product of the number of trees in each cardinal direction
        scenic_score: int = 1
        for cardinal_direction, cardinal_trees in cardinal_neighbours.items():
            # count the number of trees in each cardinal direction
            cardinal_tree_count: int = 0

            for candidate_tree_height in cardinal_trees:
                cardinal_tree_count += 1

                # if a tree is taller than the current tree, stop counting
                if candidate_tree_height >= tree_height_int:
                    break

            # multiply the scenic score by the number of trees in the current cardinal direction
            scenic_score *= cardinal_tree_count

        # update the max scenic score
        if scenic_score > max_scenic_score:
            max_scenic_score = scenic_score

print(f"Part 2: {max_scenic_score}")
