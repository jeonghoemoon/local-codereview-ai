"""AI prompt templates for code review tasks."""


SYSTEM_PROMPT = """You are an expert code reviewer with deep knowledge of software engineering best practices.
You provide thorough, constructive, and actionable code reviews.
Always respond in {language}.
"""

REVIEW_PROMPT = """Please review the following code and provide detailed feedback.

**File:** `{filename}`
**Language:** {code_language}

```{code_language}
{code}
```

Please analyze the code and provide feedback in the following categories:

1. **🐛 Bugs & Errors** — Potential bugs, logic errors, or edge cases
2. **⚡ Performance** — Performance issues or optimization opportunities
3. **📖 Readability** — Code clarity, naming, and documentation
4. **🏗️ Architecture** — Design patterns, modularity, and maintainability
5. **💡 Suggestions** — Specific improvement recommendations with code examples

For each issue found, include:
- Severity: 🔴 Critical / 🟡 Warning / 🔵 Info
- Line number (if identifiable)
- Description of the issue
- Suggested fix

End with an overall quality score from 1 to 10.
"""

DIFF_REVIEW_PROMPT = """Please review the following Git diff and provide feedback on the changes.

{diff_content}

Focus on:
1. **🐛 Bugs & Errors** — Bugs or issues introduced by the changes
2. **⚡ Performance** — Performance regressions
3. **🔒 Security** — Security issues introduced by the changes
4. **📖 Readability** — Readability of the changed code
5. **💡 Suggestions** — Improvements for the changed code

For each issue:
- Severity: 🔴 Critical / 🟡 Warning / 🔵 Info
- File and line context
- Description and suggested fix
"""

SECURITY_PROMPT = """You are a security expert. Analyze the following code for security vulnerabilities.

**File:** `{filename}`
**Language:** {code_language}

```{code_language}
{code}
```

Check for these categories of vulnerabilities:

1. **💉 Injection Attacks** — SQL injection, command injection, XSS, etc.
2. **🔐 Authentication & Authorization** — Weak auth, missing access control
3. **🔑 Secrets & Credentials** — Hardcoded passwords, API keys, tokens
4. **📦 Input Validation** — Missing or insufficient input validation
5. **🌐 Network Security** — Insecure HTTP, missing TLS, CORS issues
6. **📁 File Security** — Path traversal, unsafe file operations
7. **🔒 Cryptography** — Weak algorithms, improper usage
8. **💾 Data Exposure** — Sensitive data in logs, error messages

For each vulnerability found:
- Severity: 🔴 Critical / 🟡 Warning / 🔵 Info
- CWE ID (if applicable)
- Description
- Impact
- Remediation with code example

If no vulnerabilities are found, explicitly state that the code appears secure.
"""

STYLE_PROMPT = """You are a code style and conventions expert. Check the following code for style issues.

**File:** `{filename}`
**Language:** {code_language}

```{code_language}
{code}
```

Check for:

1. **📝 Naming Conventions** — Variable, function, class naming standards
2. **📏 Code Formatting** — Indentation, line length, whitespace
3. **📖 Documentation** — Missing docstrings, comments, type hints
4. **🧹 Code Cleanliness** — Dead code, unused imports, magic numbers
5. **🏛️ Best Practices** — Language-specific idioms and conventions

For each issue:
- Category and severity (🔴 Must Fix / 🟡 Should Fix / 🔵 Nice to Have)
- Line number (if identifiable)
- Current code → Suggested code

End with a style compliance score from 1 to 10.
"""

LANGUAGE_MAP = {
    "ko": "Korean (한국어)",
    "en": "English",
    "ja": "Japanese (日本語)",
    "zh": "Chinese (中文)",
}


def get_language_name(lang_code: str) -> str:
    """Get the display name for a language code."""
    return LANGUAGE_MAP.get(lang_code, "Korean (한국어)")
