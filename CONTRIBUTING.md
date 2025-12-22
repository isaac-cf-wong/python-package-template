# Contributing to package_name

🎉 Thank you for your interest in contributing to `package_name`!
Your ideas, fixes, and improvements are welcome and appreciated.

Whether you’re fixing a typo, reporting a bug, suggesting a feature, or submitting a pull request—this guide will help you get started.

## 📌 How to Contribute

1. Open an Issue

- Have a question, bug report, or feature suggestion? [Open an issue](https://github.com/isaac-cf-wong/python-package-template/issues/new/choose) and describe your idea clearly.
- Check for existing issues before opening a new one.

2. Fork and Clone the Repository

```shell
git clone git@github.com:<username>/package_name.git
cd package_name
```

3. Set Up Your Environment

We recommend using uv to manage virtual environments for installing `package_name`.
If you don't have uv installed, you can install it with pip. See the project pages for more details:

- Install via pip: `pip install --upgrade pip && pip install uv`
- Project pages: [uv on PyPI](https://pypi.org/project/uv/) | [uv on GitHub](https://github.com/astral-sh/uv)
- Full documentation and usage guide: [uv docs](https://docs.astral.sh/uv/)

```shell
# Create a virtual environment (recommended with uv)
uv venv --python 3.10
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

4. Set Up Pre-commit Hooks

We use pre-commit to ensure code quality and consistency. After installing dependencies, run:

```shell
pre-commit install
```

This ensures checks like code formatting, linting, and basic hygiene run automatically when you commit.

5. Create a New Branch

Give it a meaningful name like fix-typo-in-docs or feature-add-summary-option.

6. Make Changes

- Write clear, concise, and well-documented code.
- Follow [PEP 8](https://pep8.org/) style conventions.
- Add or update unit tests when applicable.

7. Run Tests

Ensure that all tests pass before opening a pull request:

```shell
pytest
```

8. Open a Pull Request

Clearly describe the motivation and scope of your change. Link it to the relevant issue if applicable.
The pull request titles should match the [Conventional Commits spec](https://www.conventionalcommits.org/).

## 💡 Tips

- Be kind and constructive in your communication.
- Keep PRs focused and atomic—smaller changes are easier to review.
- Document new features and update existing docs if needed.
- Tag your PR with relevant labels if you can.

## 📜 Licensing

By contributing, you agree that your contributions will be licensed under the project’s MIT License.

---

Thanks again for being part of the `package_name` community!

---
