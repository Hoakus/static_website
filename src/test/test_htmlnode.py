from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextType, TextNode
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


class TestLeafNode(unittest.TestCase):
    def test_valueless_leaf(self):
        node = LeafNode(tag="p", value=None)  # pyright: ignore
        self.assertRaises(ValueError, node.to_html)

    def test_tagless_leaf(self):
        node = LeafNode(tag=None, value="Hello, World!")  # pyright: ignore
        self.assertEqual(node.to_html(), "Hello, World!")

    def test_leaf_with_props(self):
        properties = {"href": "https://example.com/testing"}
        node = LeafNode(tag="a", value="click here", props=properties)

        answer_string = '<a href="https://example.com/testing">click here</a>'

        self.assertEqual(node.to_html(), answer_string)


class TestParentNode(unittest.TestCase):
    def test_parent_without_tag(self):
        node = ParentNode(tag=None, children=[HTMLNode()])
        self.assertRaises(ValueError, node.to_html)

    def test_parent_without_child(self):
        node = ParentNode(tag="b", children=None)  # pyright: ignore
        self.assertRaises(ValueError, node.to_html)

    def test_simple_parent(self):
        child = LeafNode(tag="p", value="I can't believe it's not butter")
        parent = ParentNode(tag="div", children=[child])

        answer_string = "<div><p>I can't believe it's not butter</p></div>"

        self.assertEqual(parent.to_html(), answer_string)

    def test_complex_parent(self):
        header_child = LeafNode("h1", "BLOGGIN BAILEY")
        child1 = LeafNode("p", "Welcome to my blog. Click the link below")
        child2 = LeafNode("a", value="MY BLOG", props={"href": "blog.com"})
        div_parent = ParentNode(
            "div", children=[child1, child2], props={"title": "blogdiv"}
        )
        body_parent = ParentNode("b", children=[header_child, div_parent])

        answer_string = ""
        answer_string += "<b>"
        answer_string += "<h1>BLOGGIN BAILEY</h1>"
        answer_string += '<div title="blogdiv">'
        answer_string += "<p>Welcome to my blog. Click the link below</p>"
        answer_string += '<a href="blog.com">MY BLOG</a>'
        answer_string += "</div>"
        answer_string += "</b>"

        self.assertEqual(body_parent.to_html(), answer_string)

    # BOOT.DEV TESTS
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def text_image(self):
        node = TextNode(
            "picture of a dolphin",
            TextType.IMAGE,
            url="https://example.com/dolphin.png",
        )
        html_node = text_node_to_html_node(node)
        answer_string = ""
        answer_string += '<img src="dolphin.png"'
        answer_string += 'alt="picture of a dolphin"></img>'
        self.assertEqual(html_node.to_html(), answer_string)
