import unittest

from textnode import TextNode, TextType, text_node_to_html_node


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

    def test_text_node_to_html_node_text(self):
        node = TextNode("text text", TextType.TEXT)
        node2 = text_node_to_html_node(node)
        self.assertEqual(repr(node2), 'LeafNode(None, text text, None)')
    def test_text_node_to_html_node_bold(self):
        node = TextNode("bold text", TextType.BOLD)
        node2 = text_node_to_html_node(node)
        self.assertEqual(repr(node2), 'LeafNode(b, bold text, None)')
    def test_text_node_to_html_node_italic(self):
        node = TextNode("italic text", TextType.ITALIC)
        node2 = text_node_to_html_node(node)
        self.assertEqual(repr(node2), 'LeafNode(it, italic text, None)')
    def test_text_node_to_html_node_code(self):
        node = TextNode("code text", TextType.CODE)
        node2 = text_node_to_html_node(node)
        self.assertEqual(repr(node2), 'LeafNode(code, code text, None)')
    def test_text_node_to_html_node_link(self):
        node = TextNode("link text", TextType.LINK, "www.foo.com")
        node2 = text_node_to_html_node(node)
        self.assertEqual(repr(node2), "LeafNode(a, link text, {'html': 'www.foo.com'})")
    def test_text_node_to_html_node_image(self):
        node = TextNode("image text", TextType.IMAGE, "www.bar.com")
        node2 = text_node_to_html_node(node)
        self.assertEqual(repr(node2), "LeafNode(img, image text, {'src': 'www.bar.com'})")
    
 
 
if __name__ == "__main__":
    unittest.main()