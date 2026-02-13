class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method is not implemented")
    
    def props_to_html(self):
        formatted_string = ""
        if self.props is None:
            return formatted_string
        for property in self.props:
            formatted_string = formatted_string + f' {property}="{self.props[property]}"'
        return formatted_string
    
    def __repr__(self):
        s = self.props_to_html()
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
