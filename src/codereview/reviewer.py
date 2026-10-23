"""Code review engine — core analysis logic."""

from __future__ import annotations

import os
from pathlib import Path

try:
    from rich.console import Console
    from rich.panel import Panel
    console = Console()
except ImportError:
    class DummyConsole:
        def print(self, *args, **kwargs):
            import re
            import sys
            text = " ".join(str(a) for a in args)
            clean_text = re.sub(r"\[/?[\w\s=#]+\]", "", text)
            try:
                print(clean_text)
            except UnicodeEncodeError:
                safe_text = clean_text.encode(sys.stdout.encoding or "utf-8", errors="replace").decode(sys.stdout.encoding or "utf-8")
                print(safe_text)
    class DummyPanel:
        def __init__(self, content, title="", border_style=""):
            self.content = content
            self.title = title
        def __str__(self):
            return f"=== {self.title} ===\n{self.content}"
    console = DummyConsole()
    Panel = DummyPanel

from codereview.llm_client import LLMClient
from codereview.prompts import (
    REVIEW_PROMPT,
    SECURITY_PROMPT,
    STYLE_PROMPT,
    SYSTEM_PROMPT,
    get_language_name,
)

# Map file extensions to language names
EXTENSION_MAP: dict[str, str] = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".jsx": "jsx",
    ".tsx": "tsx",
    ".java": "java",
    ".c": "c",
    ".cpp": "cpp",
    ".h": "c",
    ".hpp": "cpp",
    ".cs": "csharp",
    ".go": "go",
    ".rs": "rust",
    ".rb": "ruby",
    ".php": "php",
    ".swift": "swift",
    ".kt": "kotlin",
    ".scala": "scala",
    ".r": "r",
    ".R": "r",
    ".sql": "sql",
    ".sh": "bash",
    ".bash": "bash",
    ".html": "html",
    ".css": "css",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".json": "json",
    ".xml": "xml",
    ".md": "markdown",
    ".toml": "toml",
}


def detect_language(filepath: str) -> str:
    """Detect the programming language from the file extension.

    Args:
        filepath: Path to the source file.

    Returns:
        The detected language name.
    """
    ext = Path(filepath).suffix.lower()
    return EXTENSION_MAP.get(ext, "text")


def read_source_file(filepath: str) -> str:
    """Read source code from a file.

    Args:
        filepath: Path to the source file.

    Returns:
        The file contents as a string.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    if not path.is_file():
        raise ValueError(f"Not a file: {filepath}")

    return path.read_text(encoding="utf-8")


class CodeReviewer:
    """AI-powered code review engine."""

    def __init__(self, model: str = "codellama", lang: str = "ko"):
        """Initialize the code reviewer.

        Args:
            model: Ollama model name.
            lang: Output language code (ko, en, ja, zh).
        """
        self.client = LLMClient(model=model)
        self.lang = lang
        self.language_name = get_language_name(lang)

    def review_file(self, filepath: str) -> str:
        """Perform a full code review on a file.

        Args:
            filepath: Path to the source file.

        Returns:
            The review result text.
        """
        console.print(
            Panel(
                f"📄 Reviewing: [bold]{filepath}[/bold]",
                title="Code Review",
                border_style="blue",
            )
        )

        code = read_source_file(filepath)
        code_language = detect_language(filepath)
        filename = os.path.basename(filepath)

        system = SYSTEM_PROMPT.format(language=self.language_name)
        prompt = REVIEW_PROMPT.format(
            filename=filename,
            code_language=code_language,
            code=code,
        )

        console.print("[dim]🤖 AI analyzing code...[/dim]\n")
        return self.client.chat(system, prompt)

    def review_security(self, filepath: str) -> str:
        """Perform a security vulnerability scan on a file.

        Args:
            filepath: Path to the source file.

        Returns:
            The security review result text.
        """
        console.print(
            Panel(
                f"🔒 Security scan: [bold]{filepath}[/bold]",
                title="Security Analysis",
                border_style="red",
            )
        )

        code = read_source_file(filepath)
        code_language = detect_language(filepath)
        filename = os.path.basename(filepath)

        system = SYSTEM_PROMPT.format(language=self.language_name)
        prompt = SECURITY_PROMPT.format(
            filename=filename,
            code_language=code_language,
            code=code,
        )

        console.print("[dim]🤖 AI scanning for vulnerabilities...[/dim]\n")
        return self.client.chat(system, prompt)

    def review_style(self, filepath: str) -> str:
        """Perform a code style and convention check on a file.

        Args:
            filepath: Path to the source file.

        Returns:
            The style review result text.
        """
        console.print(
            Panel(
                f"🎨 Style check: [bold]{filepath}[/bold]",
                title="Style & Conventions",
                border_style="yellow",
            )
        )

        code = read_source_file(filepath)
        code_language = detect_language(filepath)
        filename = os.path.basename(filepath)

        system = SYSTEM_PROMPT.format(language=self.language_name)
        prompt = STYLE_PROMPT.format(
            filename=filename,
            code_language=code_language,
            code=code,
        )

        console.print("[dim]🤖 AI checking code style...[/dim]\n")
        return self.client.chat(system, prompt)

    def full_review(self, filepath: str) -> str:
        """Run all review types (review + security + style) on a file.

        Args:
            filepath: Path to the source file.

        Returns:
            Combined review results.
        """
        results = []

        console.print(
            Panel(
                f"🔍 Full analysis: [bold]{filepath}[/bold]",
                title="Full Code Analysis",
                border_style="green",
            )
        )

        # Code review
        console.print("\n[bold blue]━━━ 📄 Code Review ━━━[/bold blue]\n")
        review = self.review_file(filepath)
        results.append("## 📄 Code Review\n\n" + review)

        # Security scan
        console.print("\n[bold red]━━━ 🔒 Security Scan ━━━[/bold red]\n")
        security = self.review_security(filepath)
        results.append("## 🔒 Security Analysis\n\n" + security)

        # Style check
        console.print("\n[bold yellow]━━━ 🎨 Style Check ━━━[/bold yellow]\n")
        style = self.review_style(filepath)
        results.append("## 🎨 Style & Conventions\n\n" + style)

        return "\n\n---\n\n".join(results)
