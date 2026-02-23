import unittest

from textnode import TextNode
from textnode import TextType
from utilities import split_nodes_delimiter
from utilities import extract_markdown_images
from utilities import extract_markdown_links

class TestTextNode(unittest.TestCase):
    def test_notextnodes(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        old_nodes = [node, node2]
        expected = [TextNode("This is a text node", TextType.BOLD, None), 
                    TextNode("This is a text node", TextType.BOLD, None)]
        actual = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        self.assertEqual(expected, actual)
    def test_codeblocksinnode(self):
        node = TextNode("This is text with a `code block` word.  And `more code` too!", TextType.TEXT)
        old_nodes = [node]
        expected = [TextNode("This is text with a ", TextType.TEXT, None), 
                    TextNode("code block", TextType.CODE, None), 
                    TextNode(" word.  And ", TextType.TEXT, None), 
                    TextNode("more code", TextType.CODE, None), 
                    TextNode(" too!", TextType.TEXT, None)]
        actual = split_nodes_delimiter(old_nodes, '`', TextType.CODE)
        self.assertEqual(expected, actual)
    def test_severalnodeswithcodeblocks(self):
        old_nodes = [
                TextNode("This is `text` with a ", TextType.TEXT),
                TextNode("bolded phrase", TextType.BOLD),
                TextNode(" in `the` middle", TextType.TEXT),
                ]
        expected = [TextNode("This is ", TextType.TEXT, None), 
                    TextNode("text", TextType.CODE, None), 
                    TextNode(" with a ", TextType.TEXT, None), 
                    TextNode("bolded phrase", TextType.BOLD, None), 
                    TextNode(" in ", TextType.TEXT, None), 
                    TextNode("the", TextType.CODE, None), 
                    TextNode(" middle", TextType.TEXT, None)]
        actual = split_nodes_delimiter(old_nodes, '`', TextType.CODE)
        self.assertEqual(expected, actual)
    def test_eq2(self):
        old_nodes = [
                TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT),
                ]
        expected = [
                    TextNode("This is text with a ", TextType.TEXT),
                    TextNode("bolded phrase", TextType.BOLD),
                    TextNode(" in the middle", TextType.TEXT),
                    ]
        actual = split_nodes_delimiter(old_nodes, '**', TextType.BOLD)
        self.assertEqual(expected, actual)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
                )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
                "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
                )
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertListEqual(expected, matches)
    