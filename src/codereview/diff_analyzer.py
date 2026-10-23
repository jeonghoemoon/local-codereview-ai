"""Git diff analysis for reviewing code changes."""

from __future__ import annotations

import subprocess
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
from codereview.prompts import DIFF_REVIEW_PROMPT, SYSTEM_PROMPT, get_language_name


def run_git_command(args: list[str], cwd: str | None = None) -> str:
    """Run a git command and return the output.

    Args:
        args: Git command arguments (without 'git' prefix).
        cwd: Working directory for the command.

    Returns:
        Command stdout as a string.

    Raises:
        RuntimeError: If the git command fails.
    """
    cmd = ["git"] + args
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=cwd,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Git command failed: {' '.join(cmd)}\n{e.stderr}") from e
    except FileNotFoundError:
        raise RuntimeError("Git is not installed or not in PATH.")


def get_staged_diff(cwd: str | None = None) -> str:
    """Get the diff of staged changes.

    Args:
        cwd: Git repository working directory.

    Returns:
        The diff output.
    """
    return run_git_command(["diff", "--staged"], cwd=cwd)


def get_diff_against(ref: str = "HEAD~1", cwd: str | None = None) -> str:
    """Get the diff against a specific git reference.

    Args:
        ref: Git reference to diff against (e.g., HEAD~1, branch name).
        cwd: Git repository working directory.

    Returns:
        The diff output.
    """
    return run_git_command(["diff", ref], cwd=cwd)


def get_diff_between(ref1: str, ref2: str, cwd: str | None = None) -> str:
    """Get the diff between two git references.

    Args:
        ref1: First git reference.
        ref2: Second git reference.
        cwd: Git repository working directory.

    Returns:
        The diff output.
    """
    return run_git_command(["diff", ref1, ref2], cwd=cwd)


class DiffAnalyzer:
    """Analyzes git diffs using AI."""

    def __init__(self, model: str = "codellama", lang: str = "ko"):
        """Initialize the diff analyzer.

        Args:
            model: Ollama model name.
            lang: Output language code.
        """
        self.client = LLMClient(model=model)
        self.lang = lang
        self.language_name = get_language_name(lang)

    def review_staged(self, cwd: str | None = None) -> str:
        """Review staged git changes.

        Args:
            cwd: Git repository working directory.

        Returns:
            The review result text.
        """
        console.print(
            Panel(
                "🔄 Reviewing staged changes...",
                title="Git Diff Review",
                border_style="cyan",
            )
        )

        diff = get_staged_diff(cwd=cwd)
        if not diff.strip():
            console.print("[yellow]⚠️  No staged changes found.[/yellow]")
            console.print("[dim]   Use 'git add <file>' to stage changes.[/dim]")
            return "No staged changes to review."

        return self._review_diff(diff)

    def review_ref(self, ref: str = "HEAD~1", cwd: str | None = None) -> str:
        """Review changes against a git reference.

        Args:
            ref: Git reference to compare against.
            cwd: Git repository working directory.

        Returns:
            The review result text.
        """
        console.print(
            Panel(
                f"🔄 Reviewing changes against [bold]{ref}[/bold]",
                title="Git Diff Review",
                border_style="cyan",
            )
        )

        diff = get_diff_against(ref, cwd=cwd)
        if not diff.strip():
            console.print(f"[yellow]⚠️  No changes found against {ref}.[/yellow]")
            return f"No changes found against {ref}."

        return self._review_diff(diff)

    def review_between(
        self, ref1: str, ref2: str, cwd: str | None = None
    ) -> str:
        """Review changes between two references.

        Args:
            ref1: First git reference.
            ref2: Second git reference.
            cwd: Git repository working directory.

        Returns:
            The review result text.
        """
        console.print(
            Panel(
                f"🔄 Reviewing changes: [bold]{ref1}..{ref2}[/bold]",
                title="Git Diff Review",
                border_style="cyan",
            )
        )

        diff = get_diff_between(ref1, ref2, cwd=cwd)
        if not diff.strip():
            console.print(
                f"[yellow]⚠️  No changes found between {ref1} and {ref2}.[/yellow]"
            )
            return f"No changes found between {ref1} and {ref2}."

        return self._review_diff(diff)

    def _review_diff(self, diff: str) -> str:
        """Review a diff string with AI.

        Args:
            diff: The diff content to review.

        Returns:
            The review result text.
        """
        # Truncate very large diffs to avoid exceeding context limits
        max_chars = 8000
        if len(diff) > max_chars:
            console.print(
                f"[yellow]⚠️  Diff is large ({len(diff)} chars). "
                f"Truncating to {max_chars} chars.[/yellow]"
            )
            diff = diff[:max_chars] + "\n\n... (truncated)"

        system = SYSTEM_PROMPT.format(language=self.language_name)
        prompt = DIFF_REVIEW_PROMPT.format(diff_content=diff)

        console.print("[dim]🤖 AI analyzing changes...[/dim]\n")
        return self.client.chat(system, prompt)
