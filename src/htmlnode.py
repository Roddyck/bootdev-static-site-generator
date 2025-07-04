from __future__ import annotations
from typing import override


class HtmlNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list[HtmlNode] | None = None,
        props: dict[str, str] | None = None,
    ):
        self.tag: str | None = tag
        self.value: str | None = value
        self.children: list[HtmlNode] | None = children
        self.props: dict[str, str] | None = props

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        if self.props is None:
            return ""

        return " ".join(f'{k}="{v}"' for k, v in self.props.items())

    @override
    def __repr__(self) -> str:
        return f"HtmlNode({self.value}, {self.tag}, {self.props}, {self.children})"


class LeafNode(HtmlNode):
    def __init__(
        self, tag: str | None, value: str, props: dict[str, str] | None = None
    ):
        super().__init__(tag, value, None, props)

    @override
    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("leaf node must have a value")

        if self.tag is None:
            return self.value

        if self.props is None:
            return f"<{self.tag}>{self.value}</{self.tag}>"

        return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HtmlNode):
    def __init__(
        self, tag: str, children: list[HtmlNode], props: dict[str, str] | None = None
    ):
        super().__init__(tag, None, children, props)

    @override
    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("parent node must have a tag")

        if self.children is None:
            raise ValueError("parent node must have children")

        if self.props is not None:
            return f"<{self.tag} {self.props_to_html()}>{"".join(child.to_html() for child in self.children)}</{self.tag}>"

        return f"<{self.tag}>{"".join(child.to_html() for child in self.children)}</{self.tag}>"
