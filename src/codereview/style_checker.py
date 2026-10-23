"""Code style and convention checker module."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class StyleIssue:
    """Represents a detected style issue."""

    severity: str  # "MUST_FIX", "SHOULD_FIX", "NICE_TO_HAVE"
    category: str
    description: str
    line_number: int | None = None
    line_content: str = ""
    suggestion: str = ""


# Style rules for Python files
PYTHON_STYLE_RULES: list[dict] = [
    {
        "pattern": r"^.{120,}$",
        "category": "Line Length",
        "severity": "SHOULD_FIX",
        "description": "Line exceeds 120 characters.",
        "suggestion": "Break long lines for better readability.",
    },
    {
        "pattern": r"\t",
        "category": "Indentation",
        "severity": "MUST_FIX",
        "description": "Tab character detected. Use spaces for indentation.",
        "suggestion": "Replace tabs with 4 spaces.",
    },
    {
        "pattern": r"import \*",
        "category": "Imports",
        "severity": "SHOULD_FIX",
        "description": "Wildcard import detected.",
        "suggestion": "Import specific names instead of using '*'.",
    },
    {
        "pattern": r"except\s*:",
        "category": "Exception Handling",
        "severity": "SHOULD_FIX",
        "description": "Bare except clause catches all exceptions.",
        "suggestion": "Catch specific exceptions (e.g., except ValueError:).",
    },
    {
        "pattern": r"except Exception\s*:",
        "category": "Exception Handling",
        "severity": "NICE_TO_HAVE",
        "description": "Broad exception handling with 'Exception'.",
        "suggestion": "Consider catching more specific exception types.",
    },
    {
        "pattern": r"\s+$",
        "category": "Whitespace",
        "severity": "NICE_TO_HAVE",
        "description": "Trailing whitespace detected.",
        "suggestion": "Remove trailing whitespace.",
    },
    {
        "pattern": r"print\s*\(",
        "category": "Debugging",
        "severity": "NICE_TO_HAVE",
        "description": "print() statement detected.",
        "suggestion": "Consider using logging module instead of print().",
    },
    {
        "pattern": r"#\s*TODO|#\s*FIXME|#\s*HACK|#\s*XXX",
        "category": "TODO Comments",
        "severity": "NICE_TO_HAVE",
        "description": "TODO/FIXME comment found.",
        "suggestion": "Track these in an issue tracker.",
    },
]


def check_docstrings(code: str) -> list[StyleIssue]:
    """Check for missing docstrings in functions and classes.

    Args:
        code: Python source code.

    Returns:
        List of style issues for missing docstrings.
    """
    issues: list[StyleIssue] = []
    lines = code.split("\n")

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Check function definitions
        if stripped.startswith("def ") and not stripped.startswith("def _"):
            # Look for docstring on next non-empty line
            has_docstring = False
            for j in range(i + 1, min(i + 3, len(lines))):
                next_line = lines[j].strip()
                if next_line.startswith('"""') or next_line.startswith("'''"):
                    has_docstring = True
                    break
                if next_line and not next_line.startswith("#"):
                    break

            if not has_docstring:
                func_name = stripped.split("(")[0].replace("def ", "")
                issues.append(
                    StyleIssue(
                        severity="SHOULD_FIX",
                        category="Documentation",
                        description=f"Function '{func_name}' is missing a docstring.",
                        line_number=i + 1,
                        line_content=stripped,
                        suggestion=f'Add a docstring to describe what {func_name}() does.',
                    )
                )

        # Check class definitions
        if stripped.startswith("class "):
            has_docstring = False
            for j in range(i + 1, min(i + 3, len(lines))):
                next_line = lines[j].strip()
                if next_line.startswith('"""') or next_line.startswith("'''"):
                    has_docstring = True
                    break
                if next_line and not next_line.startswith("#"):
                    break

            if not has_docstring:
                class_name = stripped.split("(")[0].split(":")[0].replace("class ", "")
                issues.append(
                    StyleIssue(
                        severity="SHOULD_FIX",
                        category="Documentation",
                        description=f"Class '{class_name}' is missing a docstring.",
                        line_number=i + 1,
                        line_content=stripped,
                        suggestion=f"Add a docstring to describe the {class_name} class.",
                    )
                )

    return issues


def static_style_check(code: str, language: str = "python") -> list[StyleIssue]:
    """Run pattern-based style checks on code.

    Args:
        code: Source code to check.
        language: Programming language of the code.

    Returns:
        List of detected style issues.
    """
    issues: list[StyleIssue] = []
    lines = code.split("\n")

    # Select rules based on language
    rules = PYTHON_STYLE_RULES if language == "python" else PYTHON_STYLE_RULES

    for line_num, line in enumerate(lines, start=1):
        for rule in rules:
            if re.search(rule["pattern"], line):
                issues.append(
                    StyleIssue(
                        severity=rule["severity"],
                        category=rule["category"],
                        description=rule["description"],
                        line_number=line_num,
                        line_content=line.strip(),
                        suggestion=rule.get("suggestion", ""),
                    )
                )

    # Add docstring checks for Python
    if language == "python":
        issues.extend(check_docstrings(code))

    return issues


def format_style_issues(issues: list[StyleIssue]) -> str:
    """Format style issues as a readable string.

    Args:
        issues: List of style issues.

    Returns:
        Formatted string.
    """
    if not issues:
        return ""

    severity_icons = {
        "MUST_FIX": "🔴",
        "SHOULD_FIX": "🟡",
        "NICE_TO_HAVE": "🔵",
    }

    lines = ["## 🎨 Static Style Check Results\n"]
    for issue in issues:
        icon = severity_icons.get(issue.severity, "⚪")
        lines.append(f"### {icon} [{issue.severity}] {issue.category}")
        lines.append(f"- **Description:** {issue.description}")
        if issue.line_number:
            lines.append(f"- **Line {issue.line_number}:** `{issue.line_content}`")
        if issue.suggestion:
            lines.append(f"- **Suggestion:** {issue.suggestion}")
        lines.append("")

    return "\n".join(lines)
