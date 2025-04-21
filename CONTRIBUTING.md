<!--
Update `package_name` to the name of the package.

Remove the comment when this is done.
-->

# Contributing to package name

<!--
Update `package_name` to the name of the package.

Remove the comment when this is done.
-->

🎉 Thank you for your interest in contributing to `package_name`!
Your ideas, fixes, and improvements are welcome and appreciated.

Whether you’re fixing a typo, reporting a bug, suggesting a feature, or submitting a pull request—this guide will help you get started.

## 📌 How to Contribute

1. Open an Issue

<!--
- Update the link to Issue.
    - Update `username` to the user name or organization.
    - Update `package_name` to the name of the package.

Remove the comment when this is done.
-->

- Have a question, bug report, or feature suggestion? [Open an issue](https://github.com/username/package_name/issues/new/choose) and describe your idea clearly.
- Check for existing issues before opening a new one.

2. Fork and Clone the Repository

<!--
- Update the link to Issue.
    - Update `username` to the user name or organization.
    - Update `package_name` to the name of the package.

Remove the comment when this is done.
-->

```shell
git clone git@github.com:<username>/package_name.git
cd package_name
```

3. Set Up Your Environment

We recommend using a virtual environment:

```shell
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
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

<!--
Update the statement if a different license is used.

Remove the comment when this is done.
-->

By contributing, you agree that your contributions will be licensed under the project’s MIT License.

---

<!--
Update package_name to the name of the package.

Remove the comment when this is done.
-->

Thanks again for being part of the package_name community!

---
