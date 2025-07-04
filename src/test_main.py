import unittest
from main import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        markdown = """
# Title
## Subtitle
### Subsubtitle
"""
        title = extract_title(markdown)
        self.assertEqual(title, "Title")

    def test_extract_title_with_spaces(self):
        markdown = """
# Title with spaces
## Subtitle with spaces
### Subsubtitle with spaces
"""
        title = extract_title(markdown)
        self.assertEqual(title, "Title with spaces")
