import unittest
from codereview.security import static_security_scan, format_static_issues

SAMPLE_VULNERABLE_CODE = """
import os
import subprocess
from hashlib import md5

api_key = "sk-abcdef1234567890abcdef"
DEBUG = True

def bad_func(user_input):
    eval(user_input)
    os.system("ls " + user_input)
    subprocess.run("dir", shell=True)
    h = md5(b"secret").hexdigest()
"""

class TestSecurity(unittest.TestCase):
    def test_static_security_scan_detects_issues(self):
        issues = static_security_scan(SAMPLE_VULNERABLE_CODE)
        categories = {issue.category for issue in issues}
        
        self.assertIn("Hardcoded Secrets", categories)
        self.assertIn("Code Injection", categories)
        self.assertIn("Command Injection", categories)
        self.assertIn("Weak Cryptography", categories)
        self.assertIn("Debug Mode", categories)

    def test_static_security_scan_clean_code(self):
        clean_code = """
def add(a: int, b: int) -> int:
    \"\"\"Add two numbers.\"\"\"
    return a + b
"""
        issues = static_security_scan(clean_code)
        self.assertEqual(len(issues), 0)

    def test_format_static_issues(self):
        issues = static_security_scan(SAMPLE_VULNERABLE_CODE)
        formatted = format_static_issues(issues)
        self.assertIn("## 🛡️ Static Analysis Results", formatted)
        self.assertIn("Hardcoded Secrets", formatted)

if __name__ == "__main__":
    unittest.main()
