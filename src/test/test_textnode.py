import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is italic text", TextType.ITALIC)
        node2 = TextNode("This is code text", TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_url_is_none(self):
        node = TextNode("This is normal text", TextType.TEXT)
        self.assertIsNone(node.url)

    def test_url_not_none(self):
        node = TextNode(
            "Yo, check me out on insta",
            TextType.LINK,
            url="https://instagram.com/pls-kill-me-lol",
        )
        self.assertIsNotNone(node.url)


if __name__ == "__main__":
    unittest.main()
