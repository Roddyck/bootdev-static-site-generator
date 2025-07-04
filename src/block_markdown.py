import re

from enum import Enum
from htmlnode import HtmlNode, LeafNode, ParentNode
from inline_markdown import text_to_text_nodes
from textnode import text_node_to_html_node, TextNode, TextType


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = [text.strip() for text in markdown.split("\n\n") if text.strip() != ""]
    return blocks


def block_to_block_type(block: str) -> BlockType:
    header_regex = r"^(#{1,6})\s"
    if re.match(header_regex, block):
        return BlockType.HEADING

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    for line in block.split("\n"):
        if line.startswith(">"):
            return BlockType.QUOTE
        if line.startswith("-"):
            return BlockType.UNORDERED_LIST

        ordered_list_regex = r"^\d+\.\s"
        if re.match(ordered_list_regex, line):
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


# returns a single parent HtmlNode. That one parent should contain child HtmlNodes
# representing nested elements
def markdown_to_html_node(markdown: str) -> HtmlNode:
    blocks = markdown_to_blocks(markdown)
    children: list[HtmlNode] = []

    for block in blocks:
        block_type = block_to_block_type(block)
        node = block_to_html_node(block, block_type)
        children.append(node)

    return ParentNode("div", children)


def block_to_html_node(block: str, block_type: BlockType) -> HtmlNode:
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return ul_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return ol_to_html_node(block)


def paragraph_to_html_node(block: str) -> HtmlNode:
    text = " ".join(block.split("\n"))

    children = text_to_html_node(text.strip())
    return ParentNode("p", children)


def heading_to_html_node(block: str) -> HtmlNode:
    heading_parts = block.split()
    heading, heading_text = heading_parts[0], " ".join(heading_parts[1:])
    heading_level = len(heading)

    children = text_to_html_node(heading_text)
    return ParentNode(f"h{heading_level}", children)


def code_to_html_node(block: str) -> HtmlNode:
    text = block.strip("```").lstrip("\n")
    text_node = TextNode(text, TextType.TEXT)
    html_node = text_node_to_html_node(text_node)
    list_elements: list[HtmlNode] = [ParentNode("code", [html_node])]
    return ParentNode("pre", list_elements)


def quote_to_html_node(block: str) -> HtmlNode:
    text = ""
    for line in block.split("\n"):
        text += line.strip().strip(">")

    children = text_to_html_node(text)
    return ParentNode("blockquote", children)


def ul_to_html_node(block: str) -> HtmlNode:
    list_elements: list[HtmlNode] = []

    for line in block.split("\n"):
        children = text_to_html_node(line[2:])
        list_elements.append(ParentNode("li", children))

    return ParentNode("ul", list_elements)


def ol_to_html_node(block: str) -> HtmlNode:
    list_elements: list[HtmlNode] = []

    for line in block.split("\n"):
        children = text_to_html_node(line[3:])
        list_elements.append(ParentNode("li", children))

    return ParentNode("ol", list_elements)


def text_to_html_node(text: str) -> list[HtmlNode]:
    text_nodes = text_to_text_nodes(text)

    children = [text_node_to_html_node(text_node) for text_node in text_nodes]
    return children
