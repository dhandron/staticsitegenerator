import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_ABCDE(self):
        node = HTMLNode("A","B","C",{"D":"E"})
        expected =  "HTMLNode(A, B, C, {'D': 'E'})"
        self.assertEqual(repr(node), expected)
    
    def test_tag(self):
        node = HTMLNode(tag="This is the tag.")
        expected = 'HTMLNode(This is the tag., None, None, None)'
        self.assertEqual(repr(node), expected)

    def test_value(self):
        node = HTMLNode(value="This is the value.")
        expected = 'HTMLNode(None, This is the value., None, None)'
        self.assertEqual(repr(node), expected)

    def test_children(self):
        node = HTMLNode(children=[1,2,3])
        expected = 'HTMLNode(None, None, [1, 2, 3], None)'
        self.assertEqual(repr(node), expected)

    def test_props(self):
        node = HTMLNode(props={"A":"B", "C":"D"})
        expected = "HTMLNode(None, None, None, {'A': 'B', 'C': 'D'})"
        self.assertEqual(repr(node), expected)

    def test_props_to_html(self):
        node = HTMLNode("a", "link text", props={"href":"http://www.foo.com"})
        self.assertEqual(node.props_to_html(), ' href="http://www.foo.com"')

if __name__ == "__main__":
    
    unittest.main()