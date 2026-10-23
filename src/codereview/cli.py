"""CLI interface for Local CodeReview AI."""

from __future__ import annotations

import click
from rich.console import Console
from rich.panel import Panel

from codereview import __version__
from codereview.diff_analyzer import DiffAnalyzer
from codereview.report import generate_report, save_report
from codereview.reviewer import CodeReviewer
from codereview.security import format_static_issues, static_security_scan
from codereview.style_checker import (
    format_style_issues,
    static_style_check,
)

console = Console()


def print_banner() -> None:
    """Print the application banner."""
    banner = (
        "🔍 [bold blue]Local CodeReview AI[/bold blue] "
        f"v{__version__}\n"
        "[dim]AI-powered local code review tool using Ollama LLM[/dim]"
    )
    console.print(Panel(banner, border_style="bright_blue"))


@click.group()
@click.version_option(version=__version__, prog_name="codereview")
def main() -> None:
    """🔍 Local CodeReview AI — AI-powered local code review tool."""
    pass


@main.command()
@click.argument("filepath", type=click.Path(exists=True))
@click.option("--model", default="codellama", help="Ollama model name.")
@click.option("--output", "-o", default=None, help="Save report to file.")
@click.option("--lang", default="ko", help="Review language (ko/en/ja/zh).")
def review(filepath: str, model: str, output: str | None, lang: str) -> None:
    """📄 Review a source code file."""
    print_banner()

    reviewer = CodeReviewer(model=model, lang=lang)
    if not reviewer.client.check_connection():
        raise click.Abort()

    result = reviewer.review_file(filepath)

    if output:
        report = generate_report(
            title="📄 Code Review Report",
            content=result,
            filepath=filepath,
            metadata={"Model": model, "Language": lang},
        )
        save_report(report, output)


@main.command()
@click.option("--staged", is_flag=True, help="Review staged changes.")
@click.argument("ref", default="HEAD~1", required=False)
@click.option("--model", default="codellama", help="Ollama model name.")
@click.option("--output", "-o", default=None, help="Save report to file.")
@click.option("--lang", default="ko", help="Review language (ko/en/ja/zh).")
def diff(
    staged: bool, ref: str, model: str, output: str | None, lang: str
) -> None:
    """🔄 Review git diff changes."""
    print_banner()

    analyzer = DiffAnalyzer(model=model, lang=lang)
    if not analyzer.client.check_connection():
        raise click.Abort()

    if staged:
        result = analyzer.review_staged()
    else:
        result = analyzer.review_ref(ref)

    if output:
        diff_type = "Staged Changes" if staged else f"Changes vs {ref}"
        report = generate_report(
            title="🔄 Git Diff Review Report",
            content=result,
            metadata={"Model": model, "Diff Type": diff_type},
        )
        save_report(report, output)


@main.command()
@click.argument("filepath", type=click.Path(exists=True))
@click.option("--model", default="codellama", help="Ollama model name.")
@click.option("--output", "-o", default=None, help="Save report to file.")
@click.option("--lang", default="ko", help="Review language (ko/en/ja/zh).")
def security(filepath: str, model: str, output: str | None, lang: str) -> None:
    """🔒 Scan for security vulnerabilities."""
    print_banner()

    # Run static analysis first
    from codereview.reviewer import read_source_file

    code = read_source_file(filepath)
    static_issues = static_security_scan(code)

    if static_issues:
        console.print("\n[bold red]━━━ 🛡️ Static Analysis ━━━[/bold red]\n")
        static_report = format_static_issues(static_issues)
        console.print(static_report)
    else:
        console.print("\n[green]✅ No issues found in static analysis.[/green]\n")

    # Run AI analysis
    reviewer = CodeReviewer(model=model, lang=lang)
    if not reviewer.client.check_connection():
        raise click.Abort()

    result = reviewer.review_security(filepath)

    if output:
        combined = ""
        if static_issues:
            combined += format_static_issues(static_issues) + "\n\n---\n\n"
        combined += "## 🤖 AI Security Analysis\n\n" + result
        report = generate_report(
            title="🔒 Security Analysis Report",
            content=combined,
            filepath=filepath,
            metadata={"Model": model},
        )
        save_report(report, output)


@main.command()
@click.argument("filepath", type=click.Path(exists=True))
@click.option("--model", default="codellama", help="Ollama model name.")
@click.option("--output", "-o", default=None, help="Save report to file.")
@click.option("--lang", default="ko", help="Review language (ko/en/ja/zh).")
def style(filepath: str, model: str, output: str | None, lang: str) -> None:
    """🎨 Check code style and conventions."""
    print_banner()

    # Run static style checks first
    from codereview.reviewer import detect_language, read_source_file

    code = read_source_file(filepath)
    code_lang = detect_language(filepath)
    static_issues = static_style_check(code, code_lang)

    if static_issues:
        console.print("\n[bold yellow]━━━ 🎨 Static Style Check ━━━[/bold yellow]\n")
        static_report = format_style_issues(static_issues)
        console.print(static_report)
    else:
        console.print("\n[green]✅ No style issues found in static check.[/green]\n")

    # Run AI analysis
    reviewer = CodeReviewer(model=model, lang=lang)
    if not reviewer.client.check_connection():
        raise click.Abort()

    result = reviewer.review_style(filepath)

    if output:
        combined = ""
        if static_issues:
            combined += format_style_issues(static_issues) + "\n\n---\n\n"
        combined += "## 🤖 AI Style Analysis\n\n" + result
        report = generate_report(
            title="🎨 Style & Conventions Report",
            content=combined,
            filepath=filepath,
            metadata={"Model": model},
        )
        save_report(report, output)


@main.command()
@click.argument("filepath", type=click.Path(exists=True))
@click.option("--model", default="codellama", help="Ollama model name.")
@click.option("--output", "-o", default=None, help="Save report to file.")
@click.option("--lang", default="ko", help="Review language (ko/en/ja/zh).")
def full(filepath: str, model: str, output: str | None, lang: str) -> None:
    """🔍 Run full analysis (review + security + style)."""
    print_banner()

    reviewer = CodeReviewer(model=model, lang=lang)
    if not reviewer.client.check_connection():
        raise click.Abort()

    # Static analyses
    from codereview.reviewer import read_source_file

    code = read_source_file(filepath)
    code_lang = detect_language(filepath)

    static_sec = static_security_scan(code)
    static_sty = static_style_check(code, code_lang)

    # Print static results
    if static_sec:
        console.print("\n[bold red]━━━ 🛡️ Static Security ━━━[/bold red]\n")
        console.print(format_static_issues(static_sec))

    if static_sty:
        console.print("\n[bold yellow]━━━ 🎨 Static Style ━━━[/bold yellow]\n")
        console.print(format_style_issues(static_sty))

    # AI full review
    result = reviewer.full_review(filepath)

    if output:
        combined_parts = []
        if static_sec:
            combined_parts.append(format_static_issues(static_sec))
        if static_sty:
            combined_parts.append(format_style_issues(static_sty))
        combined_parts.append("## 🤖 AI Full Analysis\n\n" + result)

        report = generate_report(
            title="🔍 Full Code Analysis Report",
            content="\n\n---\n\n".join(combined_parts),
            filepath=filepath,
            metadata={"Model": model},
        )
        save_report(report, output)


# Helper import for the 'full' and 'style' commands
from codereview.reviewer import detect_language  # noqa: E402


if __name__ == "__main__":
    main()
