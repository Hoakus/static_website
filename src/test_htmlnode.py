from htmlnode import HTMLNode
import unittest


class TestHTMLNode(unittest.TestCase):
    def test_not_implemented_to_html(self):
        node = HTMLNode()
        self.assertRaises(NotImplementedError, node.to_html)

    def test_props_to_html(self):
        node = HTMLNode(
            "a",
            "Top 10 dragons",
            props={"href": "https://top10dragons.example.com", "target": "_blank"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://top10dragons.example.com" target="_blank"',
        )

    def test_children(self):
        node = HTMLNode("h1", "I am a big header")
        node2 = HTMLNode("d", children=[HTMLNode(), node])
        self.assertEqual(node, node2.children[1])  # pyright: ignore
