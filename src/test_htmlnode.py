import unittest
from htmlnode import HtmlNode, LeafNode, ParentNode


class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HtmlNode(props={"a": "b", "c": "d"})
        self.assertEqual(node.props_to_html(), 'a="b" c="d"')

    def test_props_to_html_none(self):
        node = HtmlNode()
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        node = HtmlNode(value="This is a text node", tag="p")
        self.assertEqual(repr(node), "HtmlNode(This is a text node, p, None, None)")
        node = HtmlNode(value="This is a text node", tag="p", props={"a": "b"})
        self.assertEqual(
            repr(node), "HtmlNode(This is a text node, p, {'a': 'b'}, None)"
        )
        node = HtmlNode(
            value="This is a text node",
            tag="p",
            props={"a": "b"},
            children=[HtmlNode(value="Child", tag="span")],
        )
        self.assertEqual(
            repr(node),
            "HtmlNode(This is a text node, p, {'a': 'b'}, [HtmlNode(Child, span, None, None)])",
        )


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_span(self):
        node = LeafNode("span", "Hello, world!")
        self.assertEqual(node.to_html(), "<span>Hello, world!</span>")

    def test_leaf_to_html_none(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_props(self):
        node = LeafNode("p", "Hello, world!", {"a": "b"})
        self.assertEqual(node.to_html(), '<p a="b">Hello, world!</p>')


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child", {"a": "b"})
        parent_node = ParentNode("div", [child_node], {"c": "d"})
        self.assertEqual(
            parent_node.to_html(),
            '<div c="d"><span a="b">child</span></div>',
        )


if __name__ == "__main__":
    unittest.main()
