# CI/CD and releases

This guide describes the GitHub Actions setup for this repository: testing,
security analysis, releases, documentation, and optional PyPI publishing.

## Overview

- **CI** — `pytest` on Linux, macOS, and Windows for Python 3.12, 3.13, and 3.14
  (`ci.yml`)
- **CodeQL** — scheduled and on pushes to `main` (`codeql.yml`; also invoked
  from the scheduled release pipeline)
- **Pull request titles** — Conventional Commit style
  (`semantic_pull_request.yml`)
- **Scheduled release** — weekly tag bump, GitHub release, and optional PyPI
  publish (`scheduled_release.yml`)
- **Draft release** — moving changelog preview on every push to `main`
  (`draft_release.yml`)
- **Documentation** — Zensical build and GitHub Pages deploy
  (`documentation.yml`)
- **Manual publish** — `publish.yml` and `publish_testpypi.yml` with
  `workflow_dispatch`
- **Support floor update** — monthly SPEC 0 rolling bump of runtime lower bounds
  (`support_floor_update.yml`)

Linting and formatting are enforced locally via **prek** using
`.pre-commit-config.yaml`, and on pull requests via **pre-commit.ci**, not via a
separate job in `ci.yml`. Add a workflow job if you want Ruff in CI as well.

## Workflows

### `ci.yml` (CI)

**Triggers:** `push` and `pull_request` to `main`, plus `workflow_dispatch` and
`workflow_call`.

**Steps:** checkout → `uv` → `uv sync --group dev` → `uv run pytest` → Codecov
upload.

**Matrix:** the `highest` resolution runs on Linux, macOS, and Windows for
Python 3.12–3.14. One extra `lowest-direct` cell (Ubuntu, Python 3.12) resolves
every direct dependency to its declared lower bound, so the SPEC 0 support
floors in `pyproject.toml` are proven to actually import and pass tests. Both
paths use `--upgrade` (not `--frozen`) so CI tests real resolutions rather than
the committed lock.

**Branch protection:** require the matrix jobs you care about, for example
`test (ubuntu-latest, 3.12, highest)` (exact names appear in the Actions UI).

### `codeql.yml` (CodeQL Advanced)

**Triggers:** `push` / `pull_request` to `main`, weekly schedule,
`workflow_call`.

Runs the GitHub CodeQL autobuild + analyze steps for Python.

### `semantic_pull_request.yml` (Lint PR)

**Triggers:** `pull_request_target` when a PR is opened or updated.

Validates the PR title with
[action-semantic-pull-request](https://github.com/amannn/action-semantic-pull-request).

### `scheduled_release.yml` (Scheduled Release)

**Triggers:** `cron: '0 0 * * 2'` (Tuesday 00:00 UTC) and `workflow_dispatch`.

When there are new commits since the latest tag:

1. Calls `ci.yml` and `codeql.yml`
2. Bumps the next semantic tag with `git-cliff` / `uv run git-cliff`
3. Calls `release.yml` with that tag
4. Builds wheels, runs smoke tests, and attempts `uv publish` against the
   **`pypi`** environment (with `continue-on-error: true` so missing setup does
   not fail the template)

### `release.yml` (Release)

**Triggers:** `workflow_call` (from scheduled release) or `workflow_dispatch`
with a `tag_name` input.

Uses **git-cliff-action** to render release notes, removes the `next-release`
draft if present, and creates a GitHub Release with
**softprops/action-gh-release**.

### `draft_release.yml` (Draft Release)

**Triggers:** every push to `main`.

Refreshes a **Next Release (Draft)** GitHub release whose body is the unreleased
changelog from git-cliff.

### `documentation.yml` (Documentation)

**Triggers:** `push` to `main` and `workflow_dispatch`.

Runs `uv sync --extra docs --frozen` and `uv run zensical build`, then uploads
the `site/` directory to GitHub Pages.

### `publish.yml` / `publish_testpypi.yml`

**Triggers:** `workflow_dispatch` with a tag and environment selection.

Build with `uv build`, smoke-test artifacts, then `uv publish`. These workflows
also use `continue-on-error: true` on the publish step so the template stays
green until you configure PyPI trusted publishing and GitHub environments.

### `support_floor_update.yml` (Support floor update)

**Triggers:** `cron: '0 6 1 * *'` (monthly, 1st at 06:00 UTC) and
`workflow_dispatch`.

Runs `isaac-cf-wong/dependency-support-policy-action` in `update` mode. It reads
`[tool.dependency-support-policy]` from `pyproject.toml`, raises runtime lower
bounds that have aged past the SPEC 0 window, and opens an auto-merging PR when
anything changed. See [Dependency management](#dependency-management-spec-0).

## Dependency management (SPEC 0)

Runtime lower bounds follow
[SPEC 0](https://scientific-python.org/specs/spec-0000/): each dependency's
minimum supported version rolls forward on a fixed schedule rather than tracking
the latest release. Three pieces cooperate:

- **`[tool.dependency-support-policy]` in `pyproject.toml`** — declares the
  policy (`spec0`), which groups it manages (`project`), and `lock = "minimal"`.
  Add `exclude = ["..."]` for ecosystem siblings you release in lockstep and
  want kept at latest.
- **`support_floor_update.yml`** — the monthly workflow that computes and
  applies the new floors and opens a PR.
- **`renovate.json`** — its first `packageRule` disables Renovate for
  `project.dependencies` / `project.optional-dependencies` so the two systems do
  not fight. Renovate still manages dev tooling, GitHub Actions, pre-commit, and
  the lock file. To keep a sibling package Renovate-managed, add it as
  `"!package-name"` under `matchPackageNames` on that rule and also list it in
  the policy `exclude`.

CI proves the floors are real: the `lowest-direct` matrix cell installs every
direct dependency at its declared minimum and runs the test suite.

The App token step needs repository variable `APP_ID` and secret
`APP_PRIVATE_KEY` (a GitHub App with contents + pull-requests write). Without
them the update step still runs but PR creation is skipped.

## Release process

### Repository URL in `cliff.toml`

Replace the `<REPO>` substitution in `cliff.toml` (the `postprocessors` entry
that points at `https://github.com/isaac-cf-wong/python-package-template`) with
your own GitHub URL so changelog links resolve.

### Conventional commits

git-cliff reads history in Conventional Commits form, for example:

```bash
feat: add new feature          # Minor bump
fix: fix a bug                 # Patch bump
feat!: breaking change         # Major bump
docs: update documentation     # Changelog section, may not bump
```

[Conventional Commits](https://www.conventionalcommits.org/)

### Automatic weekly release

On the cron schedule, **Scheduled Release** runs the sequence above. No UI
action is required if commits warrant a new version.

### Manual runs

- **Scheduled Release** — Actions → **Scheduled Release** → **Run workflow** to
  mimic the weekly job immediately (still subject to “new commits since last
  tag” logic).
- **Release** — supply an existing tag to regenerate release notes for that tag.
- **Publish** / **Publish TestPyPI** — build and upload a chosen tag.

## Publishing

### GitHub environments

Create environments named **`pypi`** and/or **`testpypi`** with the protection
rules you want, then configure
[trusted publishing](https://docs.pypi.org/trusted-publishers/) on PyPI to trust
this repository’s **`scheduled_release.yml`** and **`publish.yml`** (or the
TestPyPI workflow) together with the matching environment name.

### Remove `continue-on-error` for real packages

The template tolerates missing PyPI configuration. For production, remove
`continue-on-error: true` from the publish steps (for example in
`scheduled_release.yml` near the `uv publish` step, and in `publish.yml` /
`publish_testpypi.yml`) so failed uploads fail the workflow.

## Customization

### Change the release cadence

Edit the `schedule` block in `scheduled_release.yml`.

### Change Python versions for tests

Edit the `matrix.python-version` list in `ci.yml` and align `requires-python`
and classifiers in `pyproject.toml`.

### Skip CodeQL in the scheduled pipeline

Remove or gate the `codeql` job in `scheduled_release.yml` instead of editing
`ci.yml` (CodeQL is not part of `ci.yml`).

## Troubleshooting

### CI fails

- Reproduce with `uv sync --group dev --upgrade` then `uv run pytest`
- For a `lowest-direct` failure, reproduce with
  `uv sync --group dev --upgrade --resolution lowest-direct` — a floor is too
  low
- Inspect the failing OS / Python cell in the matrix

### Scheduled release does nothing

- Confirm there are commits after the latest tag (the workflow skips otherwise)
- Inspect the `check_new_commits` job output

### PyPI publish is skipped or succeeds silently

- Check for `continue-on-error: true` on publish steps
- Verify the `pypi` environment and trusted publisher mapping

## Resources

- [GitHub Actions](https://docs.github.com/en/actions)
- [git-cliff](https://git-cliff.org/)
- [Zensical](https://zensical.org/)
- [uv](https://docs.astral.sh/uv/)
