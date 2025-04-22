from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, text_node_to_html_node
from blocks import BlockType, block_to_block_type
from typing import List
import re


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnode(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def markdown_to_blocks(markdown: str):
    raw_blocks = markdown.split("\n\n")
    clean_blocks = []

    for block in raw_blocks:
        clean_block = block.strip()

        if clean_block == "":
            continue

        lines = clean_block.split("\n")
        clean_block = "\n".join([line.strip() for line in lines])

        clean_blocks.append(clean_block)

    return clean_blocks


def text_to_textnode(text):
    converted = [TextNode(text, TextType.TEXT)]
    converted = split_nodes_delimited(converted, "**", TextType.BOLD)
    converted = split_nodes_delimited(converted, "_", TextType.ITALIC)
    converted = split_nodes_delimited(converted, "`", TextType.CODE)
    converted = split_nodes_image(converted)
    converted = split_nodes_link(converted)
    return converted


def split_nodes_delimited(old_nodes: List[TextNode], delimiter, text_type: TextType):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)

        else:
            split_nodes = []
            string_list = node.text.split(delimiter)

            if len(string_list) % 2 == 0:
                raise ValueError(f"{node.text} does not contain a pair of {delimiter}")

            else:
                for index in range(0, len(string_list)):
                    string = string_list[index]
                    if string:
                        if index % 2 == 0:
                            new_node = TextNode(string, TextType.TEXT)
                        else:
                            new_node = TextNode(string, text_type)

                        split_nodes.append(new_node)

            new_nodes.extend(split_nodes)

    return new_nodes


def split_nodes_link(nodes):
    result = []
    for node in nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        links = extract_markdown_links(node.text)
        if not links:
            result.append(node)
            continue

        remaining_text = node.text

        for anchor_text, url in links:
            parts = remaining_text.split(f"[{anchor_text}]({url})", 1)
            if parts[0]:
                result.append(TextNode(parts[0], TextType.TEXT))

            result.append(TextNode(anchor_text, TextType.LINK, url))

            if len(parts) > 1:
                remaining_text = parts[1]

        if remaining_text:
            result.append(TextNode(remaining_text, TextType.TEXT))

    return result


def split_nodes_image(nodes):
    result = []
    for node in nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        images = extract_markdown_images(node.text)
        if not images:
            result.append(node)
            continue

        remaining_text = node.text

        for alt_text, url in images:
            parts = remaining_text.split(f"![{alt_text}]({url})", 1)
            if parts[0]:
                result.append(TextNode(parts[0], TextType.TEXT))

            result.append(TextNode(alt_text, TextType.IMAGE, url))

            if len(parts) > 1:
                remaining_text = parts[1]

        if remaining_text:
            result.append(TextNode(remaining_text, TextType.TEXT))

    return result


def extract_markdown_images(text):
    search = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    results = re.findall(search, text)

    return results


def extract_markdown_links(text):
    search = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    results = re.findall(search, text)

    return results
