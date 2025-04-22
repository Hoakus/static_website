import unittest
from blocks import BlockType, block_to_block_type
from helpers import markdown_to_blocks

md = """
### This is an H3 header


```This is some code block\nThis is some more code in this block```

Here is a quote from our good friend.

>Alright chumps let's do this
>Leeeeeeeerrroooooy
>MMm Jennnnkinns

- First item
- Second Item
- Third Item

1. Number one
2. Number two
3. Number three
"""

blocks = markdown_to_blocks(md)


class TestBlockToBlockType(unittest.TestCase):

    def test_header(self):
        result = block_to_block_type(blocks[0])
        self.assertEqual(BlockType.HEADING, result)

    def test_code(self):
        result = block_to_block_type(blocks[1])
        self.assertEqual(BlockType.CODE, result)

    def test_paragraph(self):
        result = block_to_block_type(blocks[2])
        self.assertEqual(BlockType.PARAGRAPH, result)

    def test_quote(self):

        result = block_to_block_type(blocks[3])
        self.assertEqual(BlockType.QUOTE, result)

    def test_unordered_list(self):
        result = block_to_block_type(blocks[4])
        self.assertEqual(BlockType.UNORDERED_LIST, result)

    def test_ordered_list(self):
        result = block_to_block_type(blocks[5])
        self.assertEqual(BlockType.ORDERED_LIST, result)
