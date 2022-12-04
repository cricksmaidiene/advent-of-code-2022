with open("input.txt") as f:
    inp_tup: list[tuple[str, str]] = [
        tuple(x.replace("\n", "").split()) for x in f.readlines()
    ]

"""
Part 1
"""

# define a mapping of game moves to their points and wins. w means wins against
rps_mapping: dict[str, dict[str, int | str]] = dict(
    A=dict(p=1, w="C", name="Rock"),
    B=dict(p=2, w="A", name="Paper"),
    C=dict(p=3, w="B", name="Scissor"),
)

# define an encoding mapping to bring my moves and elf moves to the same lang
enc_mapping: dict[str, str] = dict(X="A", Y="B", Z="C")

# define constants
draw_score: int = 3
win_score: int = 6


def calculate_score(game_round: tuple[str, str]) -> tuple[str, str, int]:
    # decoded move
    my_move_decoded: str = enc_mapping[game_round[1]]

    # begin scores with implicit choice of RPS points
    elf_points: int = rps_mapping[game_round[0]]["p"]
    my_points: int = rps_mapping[enc_mapping[game_round[1]]]["p"]

    # winning moves
    elf_win: str = rps_mapping[game_round[0]]["w"]
    my_win: str = rps_mapping[enc_mapping[game_round[1]]]["w"]

    # record moves
    elf_move, my_move = game_round[0], my_move_decoded

    if elf_move == my_move:
        # draw
        elf_points += draw_score
        my_points += draw_score

    else:

        if elf_move == my_win:
            # elf wins
            my_points += win_score

        elif my_move == elf_win:
            # my win
            elf_points += win_score

    return (*game_round, my_points)


out_tup: list[tuple[str, str, int]] = list(map(calculate_score, inp_tup))

print(
    f"Following the strategy guide, I will gain: {sum([x[-1] for x in out_tup])} points"
)

"""
Part 2
"""

# define losing moves. w means wins against. l means loses against
new_rps_mapping: dict[str, dict[str, int | str]] = dict(
    A=dict(p=1, w="C", l="B", name="Rock"),
    B=dict(p=2, w="A", l="C", name="Paper"),
    C=dict(p=3, w="B", l="A", name="Scissor"),
)


def new_calculate_score(game_round: tuple[str, str]) -> tuple[str, str, int]:
    my_score: int = 0
    round_key: str = game_round[1]
    elf_move: str = game_round[0]

    # define points and my move for win, draw and lose wrt elf's move
    rule_mapping: dict[str, int] = dict(
        X=dict(move=new_rps_mapping[elf_move]["w"], p=0),
        Y=dict(move=elf_move, p=3),
        Z=dict(move=new_rps_mapping[elf_move]["l"], p=6),
    )

    my_move: str = rule_mapping[round_key]["move"]
    # add score based on choice of rps
    my_score += new_rps_mapping[my_move]["p"]
    # add score based on win, draw, loss
    my_score += rule_mapping[round_key]["p"]

    return (*game_round, my_score)


new_out_tup: list[tuple[str, str, int]] = list(map(new_calculate_score, inp_tup))

print(
    f"Following the strategy guide, I will gain: {sum([x[-1] for x in new_out_tup])} points"
)
