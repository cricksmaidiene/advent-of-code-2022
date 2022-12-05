with open("input.txt") as f:
    inp: list[str] = f.readlines()
    inp_cl: list[str] = [x.replace("\n", "") for x in inp]

"""
Part 1
"""

block_list: list[list[int] | None] = []
block: list[int | None] = []

for x in inp_cl:
    if not x:
        block_list.append(block)
        block = []
    else:
        block.append(int(x))

block_sums: list[int] = [sum(x) for x in block_list]
max_elf: int = max(block_sums)

print(max_elf)

"""
Part 2
"""
print(sum(sorted(block_sums)[-3:]))
