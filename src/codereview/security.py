"""Security vulnerability detection module."""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class SecurityIssue:
    """Represents a detected security issue."""

    severity: str  # "CRITICAL", "WARNING", "INFO"
    category: str
    description: str
    line_number: int | None = None
    line_content: str = ""
    cwe_id: str = ""
    suggestion: str = ""


# Pattern-based rules for quick static checks (runs before AI analysis)
SECURITY_PATTERNS: list[dict] = [
    {
        "pattern": r"eval\s*\(",
        "category": "Code Injection",
        "severity": "CRITICAL",
        "description": "Use of eval() can lead to arbitrary code execution.",
        "cwe": "CWE-95",
        "suggestion": "Avoid eval(). Use ast.literal_eval() for parsing literals.",
    },
    {
        "pattern": r"exec\s*\(",
        "category": "Code Injection",
        "severity": "CRITICAL",
        "description": "Use of exec() can lead to arbitrary code execution.",
        "cwe": "CWE-95",
        "suggestion": "Avoid exec(). Refactor to use safer alternatives.",
    },
    {
        "pattern": r"subprocess\.\w+\(.*shell\s*=\s*True",
        "category": "Command Injection",
        "severity": "CRITICAL",
        "description": "shell=True in subprocess can allow command injection.",
        "cwe": "CWE-78",
        "suggestion": "Use shell=False and pass arguments as a list.",
    },
    {
        "pattern": r"os\.system\s*\(",
        "category": "Command Injection",
        "severity": "CRITICAL",
        "description": "os.system() is vulnerable to command injection.",
        "cwe": "CWE-78",
        "suggestion": "Use subprocess.run() with shell=False instead.",
    },
    {
        "pattern": r"""(password|passwd|secret|api_key|apikey|token)\s*=\s*['\"][^'"]+['\"]""",
        "category": "Hardcoded Secrets",
        "severity": "CRITICAL",
        "description": "Potential hardcoded secret or credential detected.",
        "cwe": "CWE-798",
        "suggestion": "Use environment variables or a secrets manager.",
    },
    {
        "pattern": r"pickle\.loads?\s*\(",
        "category": "Deserialization",
        "severity": "WARNING",
        "description": "Pickle deserialization of untrusted data can execute arbitrary code.",
        "cwe": "CWE-502",
        "suggestion": "Use JSON or other safe serialization formats for untrusted data.",
    },
    {
        "pattern": r"yaml\.load\s*\(",
        "category": "Deserialization",
        "severity": "WARNING",
        "description": "yaml.load() without Loader is unsafe.",
        "cwe": "CWE-502",
        "suggestion": "Use yaml.safe_load() instead.",
    },
    {
        "pattern": r"http://",
        "category": "Insecure Communication",
        "severity": "WARNING",
        "description": "HTTP URL detected. Consider using HTTPS.",
        "cwe": "CWE-319",
        "suggestion": "Use https:// for secure communication.",
    },
    {
        "pattern": r"verify\s*=\s*False",
        "category": "TLS Verification",
        "severity": "WARNING",
        "description": "SSL/TLS verification is disabled.",
        "cwe": "CWE-295",
        "suggestion": "Enable SSL verification (verify=True).",
    },
    {
        "pattern": r"(md5|sha1)\s*\(",
        "category": "Weak Cryptography",
        "severity": "WARNING",
        "description": "Weak hash algorithm detected (MD5/SHA1).",
        "cwe": "CWE-328",
        "suggestion": "Use SHA-256 or stronger hash algorithms.",
    },
    {
        "pattern": r"\.format\s*\(.*\)\s*$",
        "category": "Format String",
        "severity": "INFO",
        "description": "String formatting with user input may be vulnerable.",
        "cwe": "CWE-134",
        "suggestion": "Validate inputs before using in format strings.",
    },
    {
        "pattern": r"DEBUG\s*=\s*True",
        "category": "Debug Mode",
        "severity": "WARNING",
        "description": "Debug mode is enabled. Disable in production.",
        "cwe": "CWE-489",
        "suggestion": "Set DEBUG = False in production.",
    },
]


def static_security_scan(code: str) -> list[SecurityIssue]:
    """Run pattern-based static security checks on code.

    Args:
        code: Source code to scan.

    Returns:
        List of detected security issues.
    """
    issues: list[SecurityIssue] = []
    lines = code.split("\n")

    for line_num, line in enumerate(lines, start=1):
        # Skip comments
        stripped = line.strip()
        if stripped.startswith("#") or stripped.startswith("//"):
            continue

        for rule in SECURITY_PATTERNS:
            if re.search(rule["pattern"], line, re.IGNORECASE):
                issues.append(
                    SecurityIssue(
                        severity=rule["severity"],
                        category=rule["category"],
                        description=rule["description"],
                        line_number=line_num,
                        line_content=stripped,
                        cwe_id=rule.get("cwe", ""),
                        suggestion=rule.get("suggestion", ""),
                    )
                )

    return issues


def format_static_issues(issues: list[SecurityIssue]) -> str:
    """Format static analysis issues as a readable string.

    Args:
        issues: List of security issues.

    Returns:
        Formatted string.
    """
    if not issues:
        return ""

    severity_icons = {
        "CRITICAL": "🔴",
        "WARNING": "🟡",
        "INFO": "🔵",
    }

    lines = ["## 🛡️ Static Analysis Results\n"]
    for issue in issues:
        icon = severity_icons.get(issue.severity, "⚪")
        lines.append(f"### {icon} [{issue.severity}] {issue.category}")
        if issue.cwe_id:
            lines.append(f"- **CWE:** {issue.cwe_id}")
        lines.append(f"- **Description:** {issue.description}")
        if issue.line_number:
            lines.append(f"- **Line {issue.line_number}:** `{issue.line_content}`")
        if issue.suggestion:
            lines.append(f"- **Suggestion:** {issue.suggestion}")
        lines.append("")

    return "\n".join(lines)
