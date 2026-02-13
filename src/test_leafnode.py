import unittest

from leafnode import LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "link text", props={"href": "http://www.foo.com/index.html"})
        #self.assertEqual(node.to_html(), '<a href="http://www.foo.com/index.html">link text</a>')
        self.assertEqual(node.to_html(), '<a href="http://www.foo.com/index.html">link text</a>')

    def test_leaf_to_html_it(self):
        node = LeafNode("it", "Hello, world!")
        self.assertEqual(node.to_html(), "<it>Hello, world!</it>")

    def test_leaf_to_html_img(self):
        node = LeafNode("img", "alternate text", props={"src":"http://www.images.org"})
        self.assertEqual(node.to_html(), '<img src="http://www.images.org" alt="alternate text">')
