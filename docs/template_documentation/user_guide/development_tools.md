# Development tools

This guide covers the development tools configured in this repository:
pre-commit, Ruff, typos, Bandit, and pytest.

## Overview

- **Pre-commit**: runs hooks before each commit (and on pre-commit.ci for pull
  requests)
- **Ruff**: linter and formatter for Python
- **typos**: fast spell checker for text files (via
  [crate-ci/typos](https://github.com/crate-ci/typos))
- **Bandit**: security-oriented static analysis for Python
- **pytest**: test runner with coverage settings in `pyproject.toml`

## Pre-commit

### Setup

```bash
uv run pre-commit install
```

### Configuration

Hooks are defined in `.pre-commit-config.yaml` (Ruff, Taplo, typos, Bandit,
Prettier, markdownlint, `uv-lock`, detect-secrets, and generic file checks).

### Running hooks

```bash
uv run pre-commit run --all-files
uv run pre-commit run ruff --all-files
```

## Ruff

Configuration lives in `pyproject.toml`:

```toml
--8<-- "pyproject.toml:111:154"
```

Typical commands:

```bash
uv run ruff check --fix src tests
uv run ruff format src tests
```

## Spell checking (typos)

The **typos** hook uses `.typos.toml` at the repository root for corrections and
word allow-lists. Run the same check as CI:

```bash
uv run pre-commit run typos --all-files
```

## Bandit

```toml
--8<-- "pyproject.toml:54:58"
```

```bash
uv run bandit -r src -c pyproject.toml
```

## pytest and coverage

```toml
--8<-- "pyproject.toml:61:78"
```

```bash
uv run pytest
```

## Conventional commits and pull requests

Release notes are built with **git-cliff** from conventional commit history.
Pull request titles are validated by **Lint PR**
(`.github/workflows/semantic_pull_request.yml`) so they follow the same
vocabulary (`feat:`, `fix:`, etc.). There is no separate Node-based commitlint
hook in this template.

## CI

The **CI** workflow runs `uv sync --extra test,ci --frozen` and `uv run pytest`
on Linux, macOS, and Windows for Python 3.12–3.14. Quality gates you care about
beyond tests should be added explicitly (for example a job that runs Ruff) if
you want them on every push.

## Customizing tools

Edit `pyproject.toml` and `.pre-commit-config.yaml`, then run:

```bash
uv run pre-commit run --all-files
```

For more detail, see the [Ruff](https://docs.astral.sh/ruff/),
[Bandit](https://bandit.readthedocs.io/),
[typos](https://github.com/crate-ci/typos), and
[pre-commit](https://pre-commit.com/) documentation.
