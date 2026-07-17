#!/usr/bin/env python3
"""Validate the generated static course without third-party dependencies."""

from __future__ import annotations

import ast
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
PAGES = [
    ROOT / "index.html",
    ROOT / "start/index.html",
    ROOT / "knn/index.html",
    ROOT / "linear-regression/index.html",
    ROOT / "logistic-regression/index.html",
    ROOT / "decision-trees/index.html",
    ROOT / "random-forests/index.html",
    ROOT / "gradient-boosting/index.html",
]
VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}
FORBIDDEN_COURSE_PATTERNS = (
    r"\bnse\b",
    r"\bbse\b",
    r"\bbulk deals?\b",
    r"\bblock deals?\b",
    r"\bstock-market\b",
    r"\bstock market\b",
    r"india_bulk_block_deals",
    r"\bdeal_type\b",
    r"\bprice_inr\b",
    r"\btrade_value_crore\b",
    r"\b119156\b",
    r"\b1,19,156\b",
    r"raw\.githubusercontent\.com/.*/learn-ml-models",
)


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[str] = []
        self.errors: list[str] = []
        self.links: list[str] = []
        self.in_pre = False
        self.in_pre_code = False
        self.code_buffer: list[str] = []
        self.code_blocks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attributes = dict(attrs)
        if tag not in VOID_TAGS:
            self.stack.append(tag)
        if tag == "pre":
            self.in_pre = True
        elif tag == "code" and self.in_pre:
            self.in_pre_code = True
            self.code_buffer = []
        if tag in {"a", "link"} and attributes.get("href"):
            self.links.append(attributes["href"] or "")
        if tag == "script" and attributes.get("src"):
            self.links.append(attributes["src"] or "")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "code" and self.in_pre_code:
            self.code_blocks.append("".join(self.code_buffer))
            self.in_pre_code = False
        elif tag == "pre":
            self.in_pre = False
        if tag in VOID_TAGS:
            return
        if not self.stack:
            self.errors.append(f"unexpected closing </{tag}>")
            return
        opened = self.stack.pop()
        if opened != tag:
            self.errors.append(f"opened <{opened}> but closed </{tag}>")

    def handle_data(self, data: str) -> None:
        if self.in_pre_code:
            self.code_buffer.append(data)

    def close(self) -> None:
        super().close()
        if self.stack:
            self.errors.append("unclosed tags: " + ", ".join(self.stack[-8:]))


def local_target(page: Path, link: str) -> Path | None:
    parsed = urlsplit(link)
    if parsed.scheme or parsed.netloc or link.startswith(("#", "mailto:")):
        return None
    path_text = unquote(parsed.path)
    if not path_text:
        return None
    target = (page.parent / path_text).resolve()
    if path_text.endswith("/") or target.is_dir():
        target = target / "index.html"
    return target


def validate_page(page: Path) -> list[str]:
    failures: list[str] = []
    if not page.exists():
        return [f"missing page: {page.relative_to(ROOT)}"]

    text = page.read_text(encoding="utf-8")
    parser = PageParser()
    parser.feed(text)
    parser.close()

    for error in parser.errors:
        failures.append(f"{page.relative_to(ROOT)}: {error}")

    for link in parser.links:
        target = local_target(page, link)
        if target is not None and not target.exists():
            failures.append(
                f"{page.relative_to(ROOT)}: broken link {link!r} -> "
                f"{target.relative_to(ROOT) if ROOT in target.parents else target}"
            )

    for number, code in enumerate(parser.code_blocks, start=1):
        try:
            ast.parse(code)
        except SyntaxError as error:
            failures.append(
                f"{page.relative_to(ROOT)}: Python block {number} has "
                f"a syntax error on line {error.lineno}: {error.msg}"
            )

    lowered = text.lower()
    for pattern in FORBIDDEN_COURSE_PATTERNS:
        if re.search(pattern, lowered):
            failures.append(
                f"{page.relative_to(ROOT)}: legacy problem-specific pattern {pattern!r}"
            )

    if page != ROOT / "index.html":
        if "../assets/course.css" not in text:
            failures.append(f"{page.relative_to(ROOT)}: shared stylesheet missing")
        if "../assets/course.js" not in text:
            failures.append(f"{page.relative_to(ROOT)}: shared script missing")

    return failures


def main() -> int:
    failures: list[str] = []
    for page in PAGES:
        failures.extend(validate_page(page))

    readme = (ROOT / "README.md").read_text(encoding="utf-8").lower()
    for pattern in FORBIDDEN_COURSE_PATTERNS:
        if re.search(pattern, readme):
            failures.append(
                f"README.md: legacy problem-specific pattern {pattern!r}"
            )

    for required in (ROOT / "assets/course.css", ROOT / "assets/course.js"):
        if not required.exists():
            failures.append(f"missing shared asset: {required.relative_to(ROOT)}")

    if failures:
        print("Course validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"Validated {len(PAGES)} pages, their local links, and Python code blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
