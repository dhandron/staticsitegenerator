from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        if self.text != other.text:
            return False
        if self.text_type != other.text_type:
            return False
        if self.url != other.url:
            return False
        return True
    
    def __repr__(self):
        return f'TextNode("{self.text}", {self.text_type}, {self.url})'
    
def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        node = LeafNode(None, text_node.text)
        return node
    if text_node.text_type == TextType.BOLD:
        node = LeafNode("b", text_node.text)
        return node
    if text_node.text_type == TextType.ITALIC:
        node = LeafNode("it", text_node.text)
        return node
    if text_node.text_type == TextType.CODE:
        node = LeafNode("code", text_node.text)
        return node
    if text_node.text_type == TextType.LINK:
        node = LeafNode("a", text_node.text, props={"html":text_node.url})
        return node
    if text_node.text_type == TextType.IMAGE:
        node = LeafNode("img", text_node.text, props={"src":text_node.url})
        return node
    raise Exception("TextNode has unrecognized TextType")
    