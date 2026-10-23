# 🔍 Local CodeReview AI

[![CI](https://github.com/jeonghoemoon/local-codereview-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/jeonghoemoon/local-codereview-ai/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-green.svg)](https://ollama.ai/)

> **Privacy-first, offline AI code review CLI** powered by Ollama. Analyze code quality, detect security vulnerabilities, inspect coding conventions, and review Git diffs — 100% locally with zero cloud data leaks.

---

## ✨ Features

- 🔄 **Git Diff Review** — Review staged changes or compare against branches/commits (`HEAD~1`) with contextual focus.
- 📄 **Full File Review** — Comprehensive analysis of code structure, performance, readability, and potential bugs.
- 🔒 **Hybrid Security Scanner** — Fast regex-based static pattern matching (CWE-mapped) followed by in-depth LLM vulnerability analysis.
- 🎨 **Style & Convention Checks** — Detects naming violations, missing docstrings, bare excepts, and formatting issues.
- 📝 **Markdown Reports** — Export structured review reports directly to `.md` files for PR comments and documentation.
- 🌐 **Multilingual Output** — Get reviews in English, Korean (`ko`), Japanese (`ja`), Chinese (`zh`), and more.
- 💻 **Rich CLI Experience** — Beautiful terminal UI with streaming responses and progress panels.

---

## 🚀 Quick Start

### Prerequisites

1. **Python 3.9+**
2. **Ollama** installed and running ([Download Ollama](https://ollama.ai))

Pull your preferred coding model (e.g., `codellama`, `llama3.1`, or `qwen2.5-coder`):

```bash
ollama pull codellama
```

### Installation

Clone the repository and install it in editable mode:

```bash
git clone https://github.com/jeonghoemoon/local-codereview-ai.git
cd local-codereview-ai

# Install package
pip install -e .

# (Optional) Install development dependencies for testing
pip install -e ".[dev]"
```

---

## 📖 Usage Examples

Try reviewing the provided sample file (`examples/sample_code.py`):

### 1. Full Code Review
```bash
codereview review examples/sample_code.py
```

### 2. Git Diff Review (Staged Changes)
Stage your changes with git and run:
```bash
git add .
codereview diff --staged
```

### 3. Review Changes Against a Commit / Branch
```bash
codereview diff HEAD~1
```

### 4. Security Vulnerability Scan
```bash
codereview security examples/sample_code.py
```

### 5. Code Style & Convention Inspection
```bash
codereview style examples/sample_code.py
```

### 6. Full Analysis (Review + Security + Style) with Markdown Export
```bash
codereview full examples/sample_code.py --output report.md
```

---

## 🛠️ CLI Commands & Options

### Commands

| Command | Description | Example |
|---|---|---|
| `review` | Comprehensive code quality & bug review | `codereview review app.py` |
| `diff` | Git diff analysis (staged or revision) | `codereview diff --staged` |
| `security` | Security vulnerability inspection (Static + AI) | `codereview security server.py` |
| `style` | Code style, convention & docstring checks | `codereview style utils.py` |
| `full` | Complete analysis (Review + Security + Style) | `codereview full main.py` |

### Common Options

| Option | Short | Description | Default |
|---|---|---|---|
| `--model` | `-m` | Ollama model name to use | `codellama` |
| `--output` | `-o` | File path to export Markdown report | `None` (stdout only) |
| `--lang` | `-l` | Output language (`en`, `ko`, `ja`, `zh`) | `ko` |

---

## 🏗️ Project Architecture

```
local-codereview-ai/
├── .github/workflows/
│   └── ci.yml               # GitHub Actions CI multi-version matrix
├── src/
│   └── codereview/
│       ├── __init__.py      # Package metadata (v0.1.0)
│       ├── cli.py           # Click-based CLI entry point
│       ├── reviewer.py      # Core review engine & language detection
│       ├── diff_analyzer.py # Git diff extraction & patch review
│       ├── security.py      # Pattern-based CWE rules & security analyzer
│       ├── style_checker.py # Code convention & docstring scanner
│       ├── report.py        # Markdown report generator
│       ├── llm_client.py    # Ollama client with streaming support
│       └── prompts.py       # Prompt engineering templates
├── tests/
│   ├── test_security.py
│   ├── test_style_checker.py
│   └── test_report_and_reviewer.py
├── examples/
│   └── sample_code.py       # Sample file with intentional flaws for testing
├── pyproject.toml           # PEP 621 packaging configuration
├── README.md                # Project documentation
├── LICENSE                  # MIT License
└── CONTRIBUTING.md          # Contribution guidelines
```

---

## 🧪 Running Tests

Run the test suite using `pytest` or Python's standard `unittest`:

```bash
# Using pytest
pytest -v

# Or using unittest directly
python -m unittest discover -s tests
```

---

## 🤝 Contributing

Contributions are welcome! Please check out [CONTRIBUTING.md](CONTRIBUTING.md) for details on code style, testing, and pull requests.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
