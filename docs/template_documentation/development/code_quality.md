# Code quality

This page summarizes how quality is enforced in the repository. Day-to-day
commands are also described in
[Development tools](../user_guide/development_tools.md).

## Tools

| Concern        | Tool       | Configuration                         |
| -------------- | ---------- | ------------------------------------- |
| Lint & format  | Ruff       | `[tool.ruff]` in `pyproject.toml`     |
| Security scans | Bandit     | `[tool.bandit]` in `pyproject.toml`   |
| Spelling       | typos      | `.typos.toml`, hook in pre-commit     |
| Hygiene        | pre-commit | `.pre-commit-config.yaml`             |
| Tests          | pytest+cov | `[tool.pytest.ini_options]`, coverage |

There is **no** dedicated Pyright or mypy job in `pyproject.toml` today; add one
if you want static typing in CI.

## Ruff

```toml
--8<-- "pyproject.toml:111:154"
```

## Bandit

```toml
--8<-- "pyproject.toml:54:58"
```

## typos

Project-specific spelling rules and allowed identifiers live in `.typos.toml`.
The pre-commit hook ID is `typos`.

## Pre-commit

```yaml
--8<-- ".pre-commit-config.yaml:1:50"
```

Run everything locally:

```bash
uv run pre-commit run --all-files
```

## Coverage

```toml
--8<-- "pyproject.toml:61:65"
```

`fail_under` is set to `0` so new projects can merge before coverage is high;
raise it when your test suite matures.

## Further reading

- [Ruff](https://docs.astral.sh/ruff/)
- [Bandit](https://bandit.readthedocs.io/)
- [typos](https://github.com/crate-ci/typos)
