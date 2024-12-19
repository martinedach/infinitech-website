#!/bin/bash

# Output file
output_file="structure_and_content.txt"

# Start with the directory structure, excluding specific directories, files, and file types
echo "Directory Structure:" > "$output_file"
tree --prune -I "venv|*.pyc|alembic|static|leads.db|.git" >> "$output_file"
echo -e "\nFile Contents:\n" >> "$output_file"

# Iterate through all files, excluding specific directories, file types, and files
find . \
    \( -path "./venv" -o -path "./alembic" -o -path "./static/images" -o -path "./static" -o -path "./.git" -o -name "leads.db" \) -prune \
    -o -type f ! -name "*.pyc" ! -name "$output_file" -print | while read -r file; do
  if [[ ! "$file" =~ ^\./static/images ]]; then  # Additional regex check to exclude static/images
    echo "File: $file" >> "$output_file"
    echo "---------------------------------" >> "$output_file"
    cat "$file" >> "$output_file"
    echo -e "\n\n" >> "$output_file"
  fi
done
