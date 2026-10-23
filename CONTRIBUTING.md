# 🤝 Contributing to Local CodeReview AI

First off, thank you for considering contributing to **Local CodeReview AI**! It's people like you that make it a great tool for developers.

---

## 🐛 Reporting Bugs

Before creating bug reports, please check the [existing issues](https://github.com/jeonghoemoon/local-codereview-ai/issues) to avoid duplicates. When filing an issue, please include:
- Your OS and Python version
- Ollama version and the LLM model used (e.g., `codellama`, `llama3.1`)
- Steps to reproduce the issue
- Expected vs. actual behavior

---

## 💡 Suggesting Enhancements

Feature requests and design ideas are very welcome! Please open an issue to discuss your proposal before starting implementation.

---

## 🔧 Development Setup

1. Fork and clone the repository:
   ```bash
   git clone https://github.com/jeonghoemoon/local-codereview-ai.git
   cd local-codereview-ai
   ```

2. Create a virtual environment and install development dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e ".[dev]"
   ```

3. Run the test suite:
   ```bash
   pytest -v
   ```

---

## 📝 Pull Request Guidelines

1. Create a descriptive feature branch from `main` (`git checkout -b feature/my-new-feature`).
2. Add unit tests for any new functionality in `tests/`.
3. Ensure all existing tests pass (`pytest`).
4. Follow PEP 8 guidelines and include type hints where appropriate.
5. Write clear, semantic commit messages.
6. Open a Pull Request with a clear explanation of the changes made.

---

## 📜 License

By contributing, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).
