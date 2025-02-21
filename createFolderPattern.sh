#!/bin/bash

# Check for input parameter (the account folder name)
if [ -z "$1" ]; then
    echo "Usage: $0 account_folder_name"
    exit 1
fi

APP="$1"
BASE_DIR="apps"
TARGET_DIR="${BASE_DIR}/${APP}"

# Create the directory structure (including the new tests folder)
mkdir -p "${TARGET_DIR}"/{enums,migrations,models,serializers,versioned_api/v1/routes,views,tests}

# Create __init__.py in each directory
for dir in $(find "${TARGET_DIR}" -type d); do
    touch "$dir/__init__.py"
done

# Create the additional routers file
touch "${TARGET_DIR}/versioned_api/v1/routers.py"