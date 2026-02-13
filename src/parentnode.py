from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError(f"ParentNode {self} has no tag")
        if self.children is None:
            raise ValueError(f"ParentNode {self} has no children")
        
        html_string = f"<{self.tag}>"
        if self.children:
            for child in self.children:
                html_string += child.to_html()
        html_string += f"</{self.tag}>"

        return html_string