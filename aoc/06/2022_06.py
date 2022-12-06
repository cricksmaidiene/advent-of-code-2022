with open("input.txt") as f:
    inp: str = f.read().replace("\n", "")

"""
Part 1
"""


def detect_packet(input_str: str, distinct_characters: int) -> tuple[str, int]:
    # create a packet stream by using a sliding window of length `distinct_characters`
    stream_packets: list[str] = [
        input_str[x : x + distinct_characters] for x in range(0, len(input_str))
    ]
    # find unique characters in each stream window
    stream_sets: list[set[str]] = [set(x) for x in stream_packets]

    packet_msg, packet_indx = None, None

    # iterate until a set of length `distinct_characters` is found and then break
    for indx, x in enumerate(stream_sets):
        if len(x) == distinct_characters:
            # find the message by indexing the window stream
            packet_msg: str = stream_packets[indx]

            # indx + 1 to account for starting at 0.
            # indx + (distinct_characters - 1) to account for the length of the packet.
            packet_indx: int = indx + (distinct_characters - 1) + 1
            break

    return packet_msg, packet_indx


print(detect_packet(inp, 4))

"""
Part 2
"""

print(detect_packet(inp, 14))
