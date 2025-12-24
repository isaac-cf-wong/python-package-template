# CI/CD and Releases

This guide explains the continuous integration and deployment setup in this Python package template, including GitHub Actions workflows, release automation, and best practices.

## Overview

The template includes comprehensive CI/CD using GitHub Actions with:

- **Automated testing**: Runs on every push and pull request
- **Multi-Python support**: Tests across multiple Python versions
- **Code quality checks**: Linting, formatting, security scanning
- **Release automation**: Automatic publishing on tags with changelog generation
- **Draft releases**: Preview upcoming changes before tagging
- **Documentation deployment**: GitHub Pages integration
- **Package publishing**: Optional PyPI publishing (requires setup)

## GitHub Actions Workflows

### CI Workflow (`.github/workflows/CI.yml`)

Runs validation on pushes and pull requests:

```yaml
--8<-- ".github/workflows/CI.yml"
```

**What it does:**

- Tests across multiple Python versions (3.10, 3.11, 3.12)
- Runs pytest with coverage reporting
- Uploads coverage to Codecov
- Can be called by other workflows as a reusable workflow

### Release Workflow (`.github/workflows/release.yml`)

Creates GitHub releases when version tags are pushed:

```yaml
--8<-- ".github/workflows/release.yml"
```

**What it does:**

- Calls the CI workflow to ensure tests pass
- Generates changelog using git-cliff
- Deletes any existing draft release
- Creates a new GitHub release with the changelog

### Draft Release Workflow (`.github/workflows/draft_release.yml`)

Creates draft releases for unreleased changes:

```yaml
--8<-- ".github/workflows/draft_release.yml"
```

**What it does:**

- Runs on pushes and pull requests to main
- Generates changelog for unreleased changes
- Creates/updates a draft release named "next-release"
- Uses concurrency control to avoid conflicts

### Documentation Workflow (`.github/workflows/documentation.yml`)

Deploys documentation to GitHub Pages:

```yaml
--8<-- ".github/workflows/documentation.yml"
```

**What it does:**

- Triggers on pushes to main branch
- Builds and deploys MkDocs documentation
- Updates GitHub Pages automatically

### Publish Workflow (`.github/workflows/publish.example.yml`)

Handles package publishing to PyPI (disabled by default):

```yaml
--8<-- ".github/workflows/publish.example.yml"
```

**What it does:**

- Builds distribution packages
- Publishes to PyPI on release publication
- Publishes to TestPyPI on manual workflow dispatch

<!-- prettier-ignore-start -->

!!!note

    Rename this file from `publish.example.yml` to `publish.yml` to enable PyPI publishing

<!-- prettier-ignore-end -->

## Release Process

### Conventional Commits

The template uses conventional commits for automated changelog generation:

```bash
# Examples
git commit -m "feat: add new feature"
git commit -m "fix: resolve bug in module"
git commit -m "docs: update documentation"
git commit -m "refactor: improve code structure"
```

**Types:**

- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test additions
- `chore`: Maintenance tasks

### Version Management

Versions are managed using Git tags with Hatch-VCS:

```bash
# Create a new version tag
git tag v1.2.3
git push origin v1.2.3
```

**Automatic actions:**

1. GitHub Actions detects the tag
2. Runs full test suite via CI workflow
3. Generates changelog using git-cliff
4. Deletes any existing draft release
5. Creates GitHub release with generated changelog
6. Optionally publishes to PyPI (if publish workflow is enabled)

### Draft Releases

The template includes automatic draft release creation:

- **Triggers**: On every push and pull request to main
- **Purpose**: Preview upcoming changes before creating a version tag
- **Content**: Shows all unreleased changes using git-cliff
- **Cleanup**: Draft releases are automatically deleted when real releases are created

### Changelog Generation

Uses git-cliff for automatic changelog creation:

```bash
# Generate changelog for latest release
git cliff --latest --strip header

# Update CHANGELOG.md with all history
git cliff -o CHANGELOG.md
```

Configuration in `cliff.toml` defines:

- Commit grouping (Features, Bug Fixes, etc.)
- Release formatting
- Conventional commit parsing

## Setting Up CI/CD

### Repository Secrets

For PyPI publishing, use [trusted publishing](https://docs.pypi.org/trusted-publishers/) (recommended) instead of API tokens:

**Trusted Publishing (Recommended):**

- No API tokens needed - GitHub Actions authenticates directly with PyPI
- More secure - no long-lived secrets to manage
- Easier setup - just configure in PyPI/TestPyPI project settings

**API Tokens (Fallback):**

- **`PYPI_API_TOKEN`**: PyPI API token for publishing to production PyPI
- **`TEST_PYPI_API_TOKEN`**: TestPyPI API token for testing publishing

### Enabling PyPI Publishing

The publish workflow is disabled by default. To enable it:

1. Rename `.github/workflows/publish.example.yml` to `publish.yml`

2. **Set up trusted publishing (recommended):**

   - Go to your PyPI project settings → Publishing
   - Add GitHub as a trusted publisher:
     - Publisher: GitHub
     - Owner: `your-username`
     - Repository: `your-repo-name`
     - Workflow: `publish.yml`
   - Repeat for TestPyPI if needed

3. **Or use API tokens (fallback):**
   - Set up the required API tokens in repository secrets
   - Create PyPI and TestPyPI environments in repository settings
   - Grant appropriate permissions for publishing

**Benefits of trusted publishing:**

- No secrets management required
- Automatic authentication from GitHub Actions
- More secure than API tokens
- Follows PyPI's security best practices

### Setting Up Pre-commit.ci

For automated code quality checks on pull requests:

1. Go to [pre-commit.ci](https://pre-commit.ci/) and install the GitHub App on your repository
2. Pre-commit.ci will automatically run all pre-commit hooks on every PR
3. It can auto-fix issues and commit changes back to the PR branch
4. Configuration is already set up in `.pre-commit-config.yaml`

### Branch Protection

Set up branch protection for `main`:

1. Go to Settings → Branches
2. Add rule for `main` branch
3. Require status checks to pass
4. Require branches to be up to date

### Required Status Checks

Configure required checks:

- `test (3.10)`
- `test (3.11)`
- `test (3.12)`

## Workflow Customization

### Adding New Checks

Modify `.github/workflows/CI.yml`:

```yaml
jobs:
  test:
    steps:
      - uses: actions/checkout@v5
      - name: New Check
        run: |
          # Your custom check here
```

### Testing on Different OS

Add matrix for operating systems:

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    python-version: ["3.10", "3.11", "3.12"]
```

### Modifying Release Triggers

The release workflow triggers on version tags. To customize:

```yaml
on:
  push:
    tags:
      - "v[0-9]+.[0-9]+.[0-9]+*" # Customize tag pattern
```

### Documentation Deployment

The documentation workflow deploys on every push to main. To customize:

```yaml
on:
  push:
    branches: [main]
  pull_request: # Add PR previews
    branches: [main]
```

### Draft Release Configuration

Customize draft release behavior:

```yaml
concurrency:
  group: draft-release
  cancel-in-progress: false # Set to true to cancel in-progress runs
```

## CI Status

Monitor CI status:

- **Pull requests**: Check status checks pass
- **Main branch**: Ensure all validations pass
- **Releases**: Verify publishing succeeds

## Release Management

### Understanding Draft Releases

Before creating a real release, you can preview what changes will be included:

1. Go to your GitHub repository **Releases** page
2. Look for a release named **"Next Release (Draft)"** with tag `next-release`
3. This shows all unreleased changes based on your commits since the last tag
4. Review the changelog to ensure everything is correct

The draft release helps you:

- Verify the changelog looks good
- Catch any missing changes before tagging
- See what's going into the next version
- Plan when to release (gather feedback first if needed)

### Pre-release Checklist

Before creating a release:

1. **Review draft release**: Go to GitHub Releases and check the "Next Release (Draft)"

   - Verify all important changes are included
   - Check that the changelog is well-organized
   - Ensure no accidental commits snuck in

2. **Verify you're on the right commit**:

   ```bash
   git log --oneline -1  # Shows current commit
   git branch -v        # Verify you're on main
   ```

3. **Ensure main branch is up to date**:

   ```bash
   git pull origin main
   ```

4. **Verify all tests pass locally** (optional, but recommended):

   ```bash
   pytest
   ```

5. **Check documentation**: Ensure documentation is current and reflects new changes

### Creating Your First Release

Releasing is simple - just create a git tag and push it:

**Step 1: Decide the version number**

Follow [semantic versioning](https://semver.org/):

- `v1.0.0` - First release
- `v1.1.0` - New features added
- `v1.0.1` - Bug fixes only
- `v2.0.0` - Breaking changes

**Step 2: Create and push the tag**

```bash
# Create tag (replace v1.0.0 with your version)
git tag v1.0.0

# Push the tag to GitHub
git push origin v1.0.0
```

**Step 3: Watch the automation**

The release workflow automatically:

1. Detects the new tag
2. Runs all tests via CI workflow
3. Generates changelog from commit messages
4. Deletes the "next-release" draft
5. Creates a new GitHub release with the changelog
6. Optionally publishes to PyPI (if enabled)

You can monitor progress in the **Actions** tab on GitHub.

### Verifying the Release

After pushing the tag:

1. **Check GitHub Actions**: Go to **Actions** tab

   - Look for the workflow named after your tag or "Release"
   - Verify it completed successfully (green checkmark)

2. **Check GitHub Releases**: Go to **Releases** page

   - New release should appear with your tag
   - Changelog should be auto-generated
   - Release should show "Latest" if it's the newest

3. **Verify PyPI** (if publishing enabled):
   ```bash
   pip install your-package==1.0.0  # Should work
   ```

### Fixing Release Mistakes

**Mistake: Wrong tag created**

If you created the tag on the wrong commit:

```bash
# Delete local tag
git tag -d v1.0.0

# Delete remote tag
git push origin --delete v1.0.0

# Create tag on correct commit and push again
git tag v1.0.0
git push origin v1.0.0
```

**Mistake: Forgot to push the tag**

If you created the tag but forgot to push:

```bash
# Push the tag
git push origin v1.0.0
```

**Mistake: Need to fix the release notes**

GitHub allows editing release notes after creation:

1. Go to **Releases** page
2. Click the three dots ⋯ next to your release
3. Select **Edit release**
4. Update the description
5. Save changes

### Release Conventions

**Commit message format:**

The changelog is auto-generated from commit messages using [conventional commits](https://www.conventionalcommits.org/). Use these formats:

```bash
# New features (appear in changelog as "Features")
git commit -m "feat: add new API endpoint"

# Bug fixes (appear as "Bug Fixes")
git commit -m "fix: resolve issue with data validation"

# Documentation (usually not in changelog)
git commit -m "docs: update installation guide"

# Breaking changes (important!)
git commit -m "feat!: change API response format"  # The ! indicates breaking
```

Conventional commits help:

- Auto-generate meaningful changelogs
- Determine version bumps (major/minor/patch)
- Quickly see what changed

### Pre-release Checklist

Before creating a release:

1. **Check draft release**: Review the "Next Release (Draft)" on GitHub Releases
2. **Verify you're on main**: `git branch` and `git pull origin main`
3. **Verify tag target**: Ensure current commit is what you want to release
4. **Update docs**: Ensure documentation is current
5. **Check dependencies**: Review for security updates
6. **Manual release creation** (not recommended):
   - The automated process handles this, but you can manually edit releases if needed

### Post-release

- **Verify release**: Check that the GitHub release was created with correct changelog
- **Test installation**: `pip install your-package==1.2.3` (if publishing to PyPI)
- **Announce**: Update relevant channels with the new release

## Advanced Features

### Scheduled Builds

Run periodic checks:

```yaml
on:
  schedule:
    - cron: "0 0 * * 0" # Weekly on Sundays
```

### Dependency Updates

Use Dependabot for automated updates:

```yaml
--8<-- ".github/dependabot.yml:1:7"
```

### CodeQL Security

GitHub's advanced security analysis is **enabled by default** in the CI workflow (complements existing Bandit scans):

```yaml
--8<-- ".github/workflows/CI.yml:44:60"
```

**What it adds beyond Bandit:**

- Advanced data flow analysis for complex vulnerabilities
- Cross-file and cross-function security issues
- Integration with GitHub Security tab and alerts
- Automated dependency vulnerability scanning
- More comprehensive coverage of security issues

<!-- prettier-ignore-start -->

!!!note

    Bandit already runs in pre-commit hooks for basic security scanning. CodeQL provides deeper analysis but uses more CI resources (~2-3 minutes per run).

<!-- prettier-ignore-end -->

**Disabling CodeQL:**

If security scanning isn't critical for your project and you want to speed up CI:

1. Remove the `codeql` job from `.github/workflows/CI.yml`
2. Bandit will still run in pre-commit hooks for basic security checks
<!-- prettier-ignore-end -->

## Troubleshooting

### Common Issues

- **CI workflow fails**: Check test logs and ensure dependencies are correct
- **Release workflow fails**: Verify git-cliff configuration and tag format
- **Draft release not updating**: Check concurrency settings and workflow permissions
- **Documentation deployment fails**: Verify MkDocs configuration and GitHub Pages setup
- **Publishing fails**: Ensure PyPI trusted publishers are configured correctly (or API tokens if using fallback method)
- **Tag not recognized**: Ensure tag format matches `v[0-9]+.[0-9]+.[0-9]+*`

### Debugging Workflows

- **Re-run failed jobs**: Click "Re-run jobs" in Actions tab
- **Debug logs**: Enable debug logging with `ACTIONS_RUNNER_DEBUG=true` secret
- **Local simulation**: Use `act` tool for local testing of workflows
- **Check draft releases**: Look for "next-release" in GitHub Releases to see unreleased changes

### Performance Optimization

- **Cache dependencies**: Already configured for pip and Python packages
- **Parallel jobs**: CI runs tests in parallel across Python versions
- **Skip CI**: Add `[skip ci]` to commit messages for documentation-only changes
- **Concurrency control**: Draft releases use queuing to avoid conflicts

## Best Practices

### Commit Hygiene

- **Conventional commits**: Follow the format strictly for automated changelog generation
- **Atomic commits**: One change per commit
- **Clear messages**: Describe what and why

### Release Strategy

- **Semantic versioning**: Major.minor.patch
- **Release often**: Smaller, frequent releases
- **Pre-releases**: Use alpha/beta tags for testing
- **Draft releases**: Use the automated draft release to preview changes before tagging

### Documentation

- **Keep docs updated**: Documentation deploys automatically on main branch pushes
- **Use MkDocs**: Leverage the built-in documentation system
- **Preview changes**: Check documentation builds in pull requests

### Workflow Management

- **Reusable workflows**: CI workflow can be called by other workflows
- **Concurrency control**: Draft releases avoid conflicts with queuing
- **Optional publishing**: PyPI publishing is opt-in via workflow file renaming
- **Security**: Use repository secrets and environments for sensitive operations

### Security

- **Dependabot**: Keep dependencies updated (configured in `.github/dependabot.yml`)
- **CodeQL**: Regular security scans via GitHub Advanced Security
- **Access control**: Limit who can create releases and manage secrets
- **Token security**: Use PyPI trusted publishing instead of API tokens when possible

For more information, see [GitHub Actions documentation](https://docs.github.com/en/actions) and [Conventional Commits](https://conventionalcommits.org/).
