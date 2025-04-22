import unittest
from helpers import (
    split_nodes_delimited,
    split_nodes_image,
    split_nodes_link,
    extract_markdown_images,
    extract_markdown_links,
    text_to_textnode,
    markdown_to_blocks,
    markdown_to_html_node,
)
from textnode import TextNode, TextType


class TestMarkdownToHTMLNode(unittest.TestCase):

    def test_paragraphs(self):
        md = """
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
        ```
        This is text that _should_ remain
        the **same** even with inline stuff
        ```
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class TestTextToTextNodes(unittest.TestCase):
    def test_full_string(self):
        string = "This is **text** with an _italic_ word and a `code block`"
        string += " and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"
        string += " and a [link](https://boot.dev)"

        result_nodes = text_to_textnode(string)
        expected_output = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        self.assertEqual(result_nodes, expected_output)


class TestSplitNodesDelimited(unittest.TestCase):
    def test_basic_split(self):
        input_nodes = [TextNode("This is `code` text", TextType.TEXT)]
        expected_output = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        result = split_nodes_delimited(input_nodes, "`", TextType.CODE)
        self.assertEqual(result, expected_output)

    def test_multiple_delimiters(self):
        input_nodes = [TextNode("This is **bold** and _italic text_", TextType.TEXT)]
        expected_output = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
        ]
        result = split_nodes_delimited(input_nodes, "**", TextType.BOLD)
        result = split_nodes_delimited(result, "_", TextType.ITALIC)
        self.assertEqual(result, expected_output)

    def test_unbalanced_delimiters(self):
        input_nodes = [TextNode("This has **unbalanced delimiters", TextType.TEXT)]
        with self.assertRaises(ValueError):
            split_nodes_delimited(input_nodes, "**", TextType.BOLD)


class TestSplitNodesImages(unittest.TestCase):
    def test_single_split(self):
        string = "Wow dude! ![pic of the moon](https://photobkt.net/butt.svg)"
        input_nodes = [TextNode(string, TextType.TEXT)]

        result_nodes = split_nodes_image(input_nodes)

        expected_result = [
            TextNode("Wow dude! ", TextType.TEXT),
            TextNode(
                "pic of the moon", TextType.IMAGE, "https://photobkt.net/butt.svg"
            ),
        ]

        self.assertEqual(expected_result, result_nodes)

    def test_multiple_splits(self):
        string = "Below, you can **see a pic** of my _neighbors_ bedroom o.o "
        string += "![bedroom at night](https://photobkt.net/bedroom.png)"

        input_nodes = [TextNode(string, TextType.TEXT)]
        split_nodes = split_nodes_delimited(input_nodes, "**", TextType.BOLD)
        split_nodes = split_nodes_delimited(split_nodes, "_", TextType.ITALIC)
        result_nodes = split_nodes_image(split_nodes)

        expected_result = [
            TextNode("Below, you can ", TextType.TEXT),
            TextNode("see a pic", TextType.BOLD),
            TextNode(" of my ", TextType.TEXT),
            TextNode("neighbors", TextType.ITALIC),
            TextNode(" bedroom o.o ", TextType.TEXT),
            TextNode(
                "bedroom at night", TextType.IMAGE, "https://photobkt.net/bedroom.png"
            ),
        ]

        self.assertEqual(expected_result, result_nodes)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


class TestSplitNodesLinks(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ) and another [second link](https://i.imgur.com/3elNhQu)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu"),
            ],
            new_nodes,
        )


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_simple_text(self):
        text = """
        **Hey!** check out my blog!
        [Click here!](https://circlespace.nil/my_blog)
        """
        results = extract_markdown_links(text)
        anchor_text, url = results[0]

        self.assertEqual(len(results), 1)
        self.assertEqual(anchor_text, "Click here!")
        self.assertEqual(url, "https://circlespace.nil/my_blog")


class TestExtractMarkdownImages(unittest.TestCase):
    def test_simple_text(self):
        text = """
        **Hey!** check out my dog!
        ![picture of my dog](https://imgur.nil/my_dog)
        """
        results = extract_markdown_images(text)
        alt_text, url = results[0]

        self.assertEqual(len(results), 1)
        self.assertEqual(alt_text, "picture of my dog")
        self.assertEqual(url, "https://imgur.nil/my_dog")
