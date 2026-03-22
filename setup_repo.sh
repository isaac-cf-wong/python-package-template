#!/bin/bash

OLD_OWNER_NAME="isaac-cf-wong"

OLD_REPO_NAME="python-package-template"
OLD_REPO_NAME_NORMALIZED="${OLD_REPO_NAME//-/_}"

url=$(git config --get remote.origin.url)

NEW_OWNER_NAME=$(echo "$url" | sed -E 's#.*[:/]([^/]+)/([^/]+)\.git#\1#')
NEW_REPO_NAME=$(echo "$url" | sed -E 's#.*[:/]([^/]+)/([^/]+)\.git#\2#')

NEW_REPO_NAME_NORMALIZED="${NEW_REPO_NAME//-/_}"

if sed --version >/dev/null 2>&1; then
    # GNU sed (Linux)
    SED_INPLACE=(-i)
else
    # BSD sed (macOS)
    SED_INPLACE=(-i '')
fi

# 4. Check if the owner is set. If not, use the original name.
sed "${SED_INPLACE[@]}" "s/$OLD_OWNER_NAME/$NEW_OWNER_NAME/g" cliff.toml

find . -type d \( -name ".git" -o -name "__pycache__" -o -name ".venv" -o -name "node_modules" -o -name ".pytest_cache" \) -prune \
    -o -type f \( -name "*.py" -o -name "*.md" -o -name "*.toml" -o -name "LICENSE" \) \
    -exec sed "${SED_INPLACE[@]}" -e "s/$OLD_REPO_NAME/$NEW_REPO_NAME/g" -e "s/$OLD_REPO_NAME_NORMALIZED/$NEW_REPO_NAME_NORMALIZED/g" {} +

mv "src/$OLD_REPO_NAME_NORMALIZED" "src/$NEW_REPO_NAME_NORMALIZED"
