with open("sample_input.txt") as f:
    inp: str = f.readlines()
    inp_tup: list[str] = [x.replace("\n", "") for x in inp]

"""
Part 1
"""

cycle_register_trail: list[tuple[int, int, str]] = []
X: int = 1
cycle: int = 0

for cmd in inp_tup:
    cycle += 1
    cycle_register_trail.append((cycle, X, cmd))

    if "addx" in cmd:
        cycle += 1
        X += int(cmd.split()[-1])

        cycle_register_trail.append((cycle, X, cmd))


FILTER_CYCLES: tuple[int] = (20, 60, 100, 140, 180, 220)
filtered_signal_strength: list[int] = []

for indx, trail_state in enumerate(cycle_register_trail):
    if trail_state[0] in FILTER_CYCLES:
        if "addx" in trail_state[-1]:
            prev_trail_state: tuple[int, int, str] = cycle_register_trail[indx - 1]
            filtered_signal_strength.append(trail_state[0] * prev_trail_state[1])
        
        else:
            filtered_signal_strength.append(trail_state[0] * trail_state[1])

print(sum(filtered_signal_strength))

"""
Part 2
"""

# TODO: Bug fix hacky solution

flat_crt_matrix = ["."] * 240
sprite: tuple[int] = (0, 1, 2)

cycle: int = 0
current_cycle_div: int = 0
for cmd in inp_tup:

    cycle += 1
    flat_crt_matrix[cycle - 1] = "#" if cycle - 1 in sprite else "."
    if "addx" in cmd:
        cycle += 1
        flat_crt_matrix[cycle - 1] = "#" if cycle - 1 in sprite else "."
        addx_val = int(cmd.split()[-1])
        new_cycle_div = (cycle - 1) // 40
        if new_cycle_div != current_cycle_div:
            current_cycle_div = new_cycle_div
            shift_val = 40 * current_cycle_div
            sprite = tuple(x + addx_val + shift_val for x in sprite)
        else:
            sprite = tuple(x + addx_val for x in sprite)
    
crt_matrix: list[str] = ["".join(flat_crt_matrix[x: x+40]) for x in range(0, 240, 40)]
print("\n".join(crt_matrix))