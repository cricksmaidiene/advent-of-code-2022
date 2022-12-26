import math
import itertools

with open("input.txt") as f:
    inp: str = f.readlines()
    inp_tup_str: list[list[str]] = [x.replace("\n", "").split() for x in inp]
    # Convert the input to a list of tuples of the form (direction, distance)
    inp_tup: list[tuple[str, int]] = [(x[0], int(x[1])) for x in inp_tup_str]

"""
Part 1
"""

# Define the starting point of the coordinate reference system
start: tuple[int, int] = (0, 0)
# Define the head and tail visitation trails
head_trail: list[tuple] = [start]
tail_trail: list[tuple] = [start]

# Define the distance between the head and tail when the tail is diagonal to the head
DIAG_DIST: float = math.sqrt(2)
KNIGHT_DIST: float = math.sqrt(5)

# Define the distance between the head and tail when the tail is cardinal to the head
STANDARD_HEAD_TAIL_DIST: int = 2

# Define the direction map for the head and tail when the head is cardinal to the tail
DIRECTION_MAP: dict = dict(U=(0, 1), D=(0, -1), L=(-1, 0), R=(1, 0))
# Define the direction map for the tail when the head is diagonal to the tail
TAIL_DIAG_MAP: dict = dict(UR=(1, 1), UL=(-1, 1), DR=(1, -1), DL=(-1, -1))


def compute_distance(head_loc: tuple, tail_loc: tuple) -> float:
    """Compute the euclidean distance between two points.

    Args:
        head_loc (tuple): The head location as a tuple of integers.
        tail_loc (tuple): The tail location as a tuple of integers.

    Returns:
        float: The euclidean distance between the two points.
    """
    return math.sqrt(
        (head_loc[0] - tail_loc[0]) ** 2 + (head_loc[1] - tail_loc[1]) ** 2
    )


def is_tail_and_head_adjacent(head_loc: tuple, tail_loc: tuple) -> bool:
    """Determine if the head and tail are adjacent, even diagonally.
    If the head and tail are adjacent, the distance between them will be 1.0
    or sqrt(2) if diagonally adjacent.

    Args:
        head_loc (tuple): The head location as a tuple of integers.
        tail_loc (tuple): The tail location as a tuple of integers.

    Returns:
        bool: True if the head and tail are adjacent, False otherwise.
    """
    return compute_distance(head_loc, tail_loc) in (1.0, DIAG_DIST)


def compute_tail_move(
    new_head_loc: tuple, tail_loc: tuple, direction: str
) -> tuple[int, int]:
    """Compute the new tail location based on the new head location and
    the old tail location. This function decides how the tail
    should move and in what direction

    Args:
        new_head_loc (tuple): The new head location as a tuple of integers.
        tail_loc (tuple): The old tail location as a tuple of integers.
        direction (str): The direction the head is moving in.

    Returns:
        tuple[int, int]: The new tail location as a tuple of integers.
    """
    dist: float = compute_distance(new_head_loc, tail_loc)
    new_tail_loc: tuple[int, int] = tail_loc

    # If the distance between the head and tail is sqrt(5), the tail should move diagonally
    if dist == KNIGHT_DIST:
        # Find the key to use for diagonal movement of the tail
        cardinality: str = ""
        # Determine if the tail should move up or down
        cardinality += "U" if new_head_loc[1] > tail_loc[1] else "D"
        # Determine if the tail should move right or left
        cardinality += "R" if new_head_loc[0] > tail_loc[0] else "L"

        # Compute the new tail location
        new_tail_loc = (
            tail_loc[0] + TAIL_DIAG_MAP[cardinality][0],
            tail_loc[1] + TAIL_DIAG_MAP[cardinality][1],
        )

    # If the distance between the head and tail is 2, the tail should move in the same direction as the head
    elif dist == STANDARD_HEAD_TAIL_DIST:
        # Compute the new tail location
        new_tail_loc = (
            tail_loc[0] + DIRECTION_MAP[direction][0],
            tail_loc[1] + DIRECTION_MAP[direction][1],
        )

    return new_tail_loc


def compute_move(direction: str, distance: int):
    """Compute the new head and tail locations based on the direction and distance.
    This function requires the global variables `head_trail` and `tail_trail` to be defined.

    Args:
        direction (str): The direction the head is moving in.
        distance (int): The number of steps taken by the head in `direction`.
    """
    for _ in range(1, distance + 1):
        # Get the current head and tail locations
        current_head_loc: tuple[int, int] = head_trail[-1]
        current_tail_loc: tuple[int, int] = tail_trail[-1]

        # Compute the new head location
        new_head_loc: tuple[int, int] = (
            current_head_loc[0] + DIRECTION_MAP[direction][0],
            current_head_loc[1] + DIRECTION_MAP[direction][1],
        )
        head_trail.append(new_head_loc)

        # Compute the new tail location
        new_tail_loc = current_tail_loc
        if not is_tail_and_head_adjacent(new_head_loc, current_tail_loc):
            new_tail_loc = compute_tail_move(new_head_loc, current_tail_loc, direction)

        tail_trail.append(new_tail_loc)


# Map the input to the compute_move function
list(itertools.starmap(compute_move, inp_tup))
# Print the length of the set of tail locations to see unique visits
print("Part 1:", len(set(tail_trail)))
