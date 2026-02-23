import re

from textnode import TextNode
from textnode import TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):

    def split_one_node(text_node, delimiter, text_type):
        node_list = []
        print(text_node.text)
        string_list = text_node.text.split(delimiter, maxsplit=2)
        if len(string_list) == 2:
            raise Exception(f"Unmatched delimiter {delimiter} in node {text_node}")
        elif len(string_list) == 1:
            return [TextNode(string_list[0], TextType.TEXT)]
        else: 
            node_list.append(TextNode(string_list[0], TextType.TEXT)) 
            node_list.append(TextNode(string_list[1], text_type))
            node_list.extend(split_one_node(TextNode(string_list[2], TextType.TEXT), delimiter, text_type))
        return node_list

#    return split_one_node(old_nodes[0], delimiter, text_type)


    new_nodes = []
    for node in old_nodes:
        if node.text_type is TextType.TEXT:
            new_nodes.extend(split_one_node(node, delimiter, text_type))
        else:
            new_nodes.append(node)
    
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches