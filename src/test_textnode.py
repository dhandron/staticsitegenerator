import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_explicit_missing_url(self):
        node = TextNode("sample text", TextType.ITALIC, None)
        node2 = TextNode("sample text", TextType.ITALIC)
        self.assertEqual(node, node2)
    def test_different_text(self):
        node = TextNode("sample text", TextType.ITALIC)
        node2 = TextNode("different text", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    def test_different_texttype(self):
        node = TextNode("sample text", TextType.ITALIC)
        node2 = TextNode("sample text", TextType.CODE)
        self.assertNotEqual(node, node2)
    def test_different_url(self):
        node = TextNode("sample text", TextType.LINK, "http://foo.com")
        node2 = TextNode("different text", TextType.LINK, "http://bar.com")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()