import unittest
from codereview.style_checker import static_style_check, format_style_issues

SAMPLE_STYLE_CODE = """
import *

def undocumented_func(x):
    try:
        y = x + 1
        print(y)
    except:
        pass
"""

class TestStyleChecker(unittest.TestCase):
    def test_static_style_check(self):
        issues = static_style_check(SAMPLE_STYLE_CODE, language="python")
        categories = {issue.category for issue in issues}

        self.assertIn("Imports", categories)
        self.assertIn("Documentation", categories)
        self.assertIn("Exception Handling", categories)
        self.assertIn("Debugging", categories)

    def test_format_style_issues(self):
        issues = static_style_check(SAMPLE_STYLE_CODE, language="python")
        formatted = format_style_issues(issues)
        self.assertIn("## 🎨 Static Style Check Results", formatted)
        self.assertIn("Documentation", formatted)

if __name__ == "__main__":
    unittest.main()
