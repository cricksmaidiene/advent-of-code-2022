from typing import Callable
from tqdm import tqdm

with open("input.txt") as f:
    inp: str = f.read()

inp_list: list[str] = inp.split("\n\n")
inp_nested_list: list[list[str]] = [x.split("\n") for x in inp_list]
inp_nested_list_cleaned: list[list[str]] = [
    [y.strip() for y in x] for x in inp_nested_list
]

monkeys: list[dict] = []

for x in inp_nested_list_cleaned:
    monkey_id: int = int(x[0].split()[-1].replace(":", ""))
    items: list[int] = [int(it) for it in x[1].split(":")[-1].strip().split(",")]
    operation_text: str = x[2].split(":")[-1].strip()
    test_divisibility: int = int(x[3].split(":")[-1].split("by")[-1].strip())
    monkey_on_true: int = int(x[4].split(":")[-1].split("to monkey")[-1].strip())
    monkey_on_false: int = int(x[5].split(":")[-1].split("to monkey")[-1].strip())

    monkey_dict: dict[str, int | list | str] = dict(
        monkey_id=monkey_id,
        items=items,
        operation_text=operation_text,
        test_divisibility=test_divisibility,
        monkey_on_true=monkey_on_true,
        monkey_on_false=monkey_on_false,
    )

    monkeys.append(monkey_dict)


intact_item_worry_decrement: Callable = lambda it_worry_level: it_worry_level // 3
is_divisible: Callable = lambda input, divisiblity: input % divisiblity == 0


def parse_and_run_operation(operations_text: str, worry_level: int) -> int:
    """Take a string containing a binary operation and return the result.
    Identify where to use variables and where to use constants.
    Returns the worry level based on the operation syntax specified.

    Args:
        operations_text (str): The binary operation to be performed.
        worry_level (int): The worry level to be used in the operation.

    Returns:
        int: The result of the operation.
    """
    binary_op: str = operations_text.split("=")[-1].strip()
    operand_x_str: str = binary_op.split()[0].strip()
    operand_y_str: str = binary_op.split()[2].strip()

    operator: str = binary_op.split()[1].strip()
    operator_map = {
        "+": lambda x, y: x + y,
        "-": lambda x, y: x - y,
        "*": lambda x, y: x * y,
        "/": lambda x, y: x / y,
    }

    try:
        operand_x = int(operand_x_str)
    except ValueError:
        operand_x = worry_level

    try:
        operand_y = int(operand_y_str)
    except ValueError:
        operand_y = worry_level

    return operator_map[operator](operand_x, operand_y)


def enact_single_monkey(monkey: dict, intact_worry_decrement: bool = True):
    """Enact a single monkey's operations on its items.

    Args:
        monkey (dict): The monkey to enact.
        intact_worry_decrement (bool, optional): Whether to decrement the worry level
            based on intact items. Defaults to True.
    """
    for it_worry_lv in monkey["items"]:
        new_it_worry_lv = parse_and_run_operation(monkey["operation_text"], it_worry_lv)
        if intact_worry_decrement:
            new_it_worry_lv: int = intact_item_worry_decrement(new_it_worry_lv)

        if is_divisible(new_it_worry_lv, monkey["test_divisibility"]):
            monkeys[monkey["monkey_on_true"]]["items"].append(new_it_worry_lv)
        else:
            monkeys[monkey["monkey_on_false"]]["items"].append(new_it_worry_lv)

    monkeys[monkey["monkey_id"]]["items"] = []


def enact_all_monkeys(iterations: int, intact_worry_decrement: bool = True) -> dict:
    """Enact all monkeys' operations on their items.
    Count the frequency with which each monkey interacts with items
    and return a dictionary of monkey_id: frequency.

    Args:
        iterations (int): The number of iterations to enact.
        intact_worry_decrement (bool, optional): Whether to decrement the worry level
            based on intact items. Defaults to True.

    Returns:
        dict: A dictionary of monkey_id: frequency.
    """
    monkey_freq_map: dict[int, int] = {monkey["monkey_id"]: 0 for monkey in monkeys}

    for x in tqdm(range(iterations)):
        if x == 100:
            input("Press enter to continue...")
        for monkey in monkeys:
            monkey_freq_map[monkey["monkey_id"]] += len(monkey["items"])
            enact_single_monkey(
                monkey=monkey, intact_worry_decrement=intact_worry_decrement
            )

    return monkey_freq_map


"""
Part 1
"""

monkey_freq_map: dict = enact_all_monkeys(iterations=20)
ordered_monkey_freqs: list[tuple[int, int]] = sorted(
    ((v, k) for k, v in monkey_freq_map.items())
)
print(ordered_monkey_freqs[-1][0] * ordered_monkey_freqs[-2][0])


"""
Part 2
Slow: Needs Rework
"""

monkey_freq_map_wo_intact: dict = enact_all_monkeys(
    iterations=10_000, intact_worry_decrement=False
)
ordered_monkey_freqs_wo_intact: list[tuple[int, int]] = sorted(
    ((v, k) for k, v in monkey_freq_map_wo_intact.items())
)
print(ordered_monkey_freqs_wo_intact[-1][0] * ordered_monkey_freqs_wo_intact[-2][0])
