#!/bin/bash
# Run Bandit security scanner on Python files

set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <file_or_directory> [output_file]"
    exit 1
fi

TARGET="$1"
OUTPUT="${2:-bandit_results.json}"

# Run bandit with JSON output
# -ll: Only report issues with severity level LOW or higher
# -f json: Output format

bandit \
    -r \
    -f json \
    -o "$OUTPUT" \
    -ll \
    "$TARGET"

echo "Bandit scan complete. Results saved to $OUTPUT"
