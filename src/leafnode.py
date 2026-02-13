from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("value is None")
        if self.tag is None:
            return self.value
        if self.tag == "a":
            s = self.props_to_html()
            return f"<a{s}>{self.value}</a>"
        if self.tag == "img":
            props = self.props_to_html()
            return f'<img{props} alt="{self.value}">'
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"