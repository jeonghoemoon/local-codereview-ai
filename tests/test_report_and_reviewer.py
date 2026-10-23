import unittest
from unittest.mock import MagicMock, patch
from codereview.report import generate_report
from codereview.reviewer import detect_language, CodeReviewer

class TestReportAndReviewer(unittest.TestCase):
    def test_detect_language(self):
        self.assertEqual(detect_language("app.py"), "python")
        self.assertEqual(detect_language("script.js"), "javascript")
        self.assertEqual(detect_language("Main.java"), "java")
        self.assertEqual(detect_language("unknown.xyz"), "text")

    def test_generate_report(self):
        report = generate_report(
            title="Test Report",
            content="Everything looks good.",
            filepath="test.py",
            metadata={"Model": "codellama"}
        )
        self.assertIn("# Test Report", report)
        self.assertIn("**File:** `test.py`", report)
        self.assertIn("**Model:** codellama", report)
        self.assertIn("Everything looks good.", report)

    @patch("codereview.reviewer.LLMClient")
    def test_code_reviewer_mock(self, mock_client_class):
        mock_instance = MagicMock()
        mock_instance.chat.return_value = "Mocked Review Output"
        mock_client_class.return_value = mock_instance

        reviewer = CodeReviewer(model="codellama", lang="ko")
        result = reviewer.review_file("examples/sample_code.py")

        self.assertEqual(result, "Mocked Review Output")
        self.assertTrue(mock_instance.chat.called)

if __name__ == "__main__":
    unittest.main()
