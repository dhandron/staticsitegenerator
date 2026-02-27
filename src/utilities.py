import re

from textnode import TextNode
from textnode import TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):

    def split_one_node(text_node, delimiter, text_type):
        if text_node.text == "":
            return []
        
        node_list = []
        #print(text_node.text)
        string_list = text_node.text.split(delimiter, maxsplit=2)
        if len(string_list) == 2:
            raise Exception(f"Unmatched delimiter {delimiter} in node {text_node}")
        elif len(string_list) == 1:
            return [TextNode(string_list[0], TextType.TEXT)]
        else: 
            if string_list[0] != "":
                node_list.append(TextNode(string_list[0], TextType.TEXT)) 
            node_list.append(TextNode(string_list[1], text_type))
            node_list.extend(split_one_node(TextNode(string_list[2], TextType.TEXT), delimiter, text_type))
        return node_list



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

def split_nodes_image(old_nodes):
    
    def split_one_node_image(node):
        
        def extract_one_image(node, image_tuple):
            markdown_text = node.text
            if markdown_text == '':
                return []
            
            image_alt_text = image_tuple[0]
            image_url = image_tuple[1]
            string_list = markdown_text.split(f"![{image_alt_text}]({image_url})", maxsplit=1)
            
            node_list = []
            if string_list[0] != '':
                node_list.append(TextNode(string_list[0], TextType.TEXT))
            node_list.append(TextNode(image_alt_text, TextType.IMAGE, image_url))
            if string_list[1] != '':
                node_list.append(TextNode(string_list[1], TextType.TEXT))
            return node_list
            
        image_tuple_list = extract_markdown_images(node.text)
        current = node
        node_list = []
        
        for image_tuple in image_tuple_list:
            split_node = extract_one_image(current, image_tuple)
            if split_node[-1].text_type == TextType.TEXT:
                node_list.extend(split_node[:-1])
                current = split_node[-1]
            else:
                node_list.extend(split_node)
                current = None
        if current is not None:
            node_list.append(current)
        
        return node_list
    
    node_list = []
    for node in old_nodes:
        node_list.extend(split_one_node_image(node))
    return node_list


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_link(old_nodes):

    def split_one_node_link(node):
        
        def extract_one_link(node, link_tuple):
            markdown_text = node.text
            if markdown_text == '':
                return []
            
            link_text = link_tuple[0]
            link_url = link_tuple[1]
            string_list = markdown_text.split(f"[{link_text}]({link_url})", maxsplit=1)
            
            node_list = []
            if string_list[0] != '':
                node_list.append(TextNode(string_list[0], TextType.TEXT))
            node_list.append(TextNode(link_text, TextType.LINK, link_url))
            if string_list[1] != '':
                node_list.append(TextNode(string_list[1], TextType.TEXT))
            return node_list
            
        link_tuple_list = extract_markdown_links(node.text)
        current = node
        node_list = []
        
        for link_tuple in link_tuple_list:
            split_node = extract_one_link(current, link_tuple)
            if split_node[-1].text_type == TextType.TEXT:
                node_list.extend(split_node[:-1])
                current = split_node[-1]
            else:
                node_list.extend(split_node)
                current = None
        if current is not None:
            node_list.append(current)
        
        return node_list
    
    node_list = []
    for node in old_nodes:
        node_list.extend(split_one_node_link(node))
    return node_list


def text_to_nodes(text):
        node = TextNode(text, TextType.TEXT)

        new_nodes = split_nodes_link([node])
        new_nodes = split_nodes_image(new_nodes)

        delimiter_list = [
            ('**', TextType.BOLD), 
            ('_', TextType.ITALIC), 
            ('`', TextType.CODE), 
            ]
        for delimiter in delimiter_list:
            new_nodes = split_nodes_delimiter(new_nodes, *delimiter)

        return new_nodes



