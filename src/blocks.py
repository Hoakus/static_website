from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "quote"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    lines = block.split("\n")
    first_line = block.split(" ")[0]

    # Headers
    if first_line.startswith("#"):
        if all(char == "#" for char in first_line):
            if 1 <= len(first_line) <= 6:
                return BlockType.HEADING

    # Code
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    # Quote
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Unordered List
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # Ordered List
    correct_sequence = []
    for index in range(0, len(lines) - 1):
        list_number = index + 1
        line = lines[index]
        if line.startswith(f"{list_number}. "):
            correct_sequence.append(True)
        else:
            correct_sequence.append(False)
    if len(correct_sequence) > 0 and all(correct_sequence):
        return BlockType.ORDERED_LIST

    # Paragraph (if nothing else matches)
    return BlockType.PARAGRAPH
