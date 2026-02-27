import unittest

from textnode import TextNode
from textnode import TextType
from utilities import split_nodes_delimiter
from utilities import extract_markdown_images
from utilities import extract_markdown_links
from utilities import split_nodes_image
from utilities import split_nodes_link
from utilities import text_to_nodes


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

    def test_eq3(self):
        old_nodes = [
                TextNode("**bolded phrase** in the middle", TextType.TEXT),
                ]
        expected = [
                    TextNode("bolded phrase", TextType.BOLD),
                    TextNode(" in the middle", TextType.TEXT),
                    ]
        actual = split_nodes_delimiter(old_nodes, '**', TextType.BOLD)
        self.assertEqual(expected, actual)

    def test_split_nodes_delimiter_noTrailingText(self):
        old_nodes = [
                TextNode("This is text with a **bolded phrase**", TextType.TEXT),
                ]
        expected = [
                    TextNode("This is text with a ", TextType.TEXT),
                    TextNode("bolded phrase", TextType.BOLD),
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


    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
            )
        actual = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ]

        self.assertListEqual(expected, actual)
    
    def test_split_images_twoNodes(self):
        node1 = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
            )
        node2 = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
            )
        actual = split_nodes_image([node1, node2])
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ]

        self.assertListEqual(expected, actual)

    def test_split_images_imageAtStart(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
            )
        actual = split_nodes_image([node])
        expected = [
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ]

        self.assertListEqual(expected, actual)

    def test_split_images_withTrailingText(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) with more text",
            TextType.TEXT,
            )
        actual = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            TextNode(" with more text", TextType.TEXT),
            ]

        self.assertListEqual(expected, actual)

    def test_split_images_withImageAndLink(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://i.imgur.com/3elNhQu.png) with more text",
            TextType.TEXT,
            )
        actual = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and a [link](https://i.imgur.com/3elNhQu.png) with more text", TextType.TEXT),
            ]

        self.assertListEqual(expected, actual)


    def test_split_linkss_withImageAndLink(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://i.imgur.com/3elNhQu.png) with more text",
            TextType.TEXT,
            )
        actual = split_nodes_link([node])
        expected = [
            TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            TextNode(" with more text", TextType.TEXT),
            ]

        self.assertListEqual(expected, actual)

    def test_split_links_withTwoLinks(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT,)
        actual = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ]

        self.assertListEqual(expected, actual)

    def test_split_linkss_withTwoLinks(self):
        node1 = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT,)
        node2 = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT,)
        actual = split_nodes_link([node1, node2])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ]

        self.assertListEqual(expected, actual)

    def test_split_linkss_withLinkAtStart(self):
        node1 = TextNode("[to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT,)
        node2 = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT,)
        actual = split_nodes_link([node1, node2])
        expected = [
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ]

        self.assertListEqual(expected, actual)

    
    def test_text_to_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        actual = text_to_nodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            ]

        self.assertListEqual(expected, actual)

    def test_text_to_nodes_boldAndItalicTogether(self):
        text = "This is **text** _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        actual = text_to_nodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            ]

        self.assertListEqual(expected, actual)

    def test_text_to_nodes_italicAndCodeTogether(self):
        text = "This is **text** with an _italic_ `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        actual = text_to_nodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            ]

        self.assertListEqual(expected, actual)

    def test_text_to_nodes_noLeadInText(self):
        text = "**text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        actual = text_to_nodes(text)
        expected = [
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            ]

        self.assertListEqual(expected, actual)

    def test_text_to_nodes_noTrailingText(self):
        text = "This is **text** _italic_ word and a `code block`"
        actual = text_to_nodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            ]

        self.assertListEqual(expected, actual)

    