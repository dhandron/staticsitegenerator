from textnode import TextNode
from textnode import TextType
from leafnode import LeafNode
from utilities import split_nodes_delimiter
from utilities import split_nodes_image
from utilities import split_nodes_link
from utilities import text_to_nodes

def main():
    text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    new_nodes = text_to_nodes(text)   
    print(new_nodes)

main()