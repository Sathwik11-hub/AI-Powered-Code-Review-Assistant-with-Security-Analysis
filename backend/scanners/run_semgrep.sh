#!/bin/bash
# Run Semgrep security scanner on a file or directory

set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <file_or_directory> [output_file]"
    exit 1
fi

TARGET="$1"
OUTPUT="${2:-semgrep_results.json}"

# Run semgrep with security rules
# Using --config=auto for automatic rule detection
# Can also use specific rulesets: --config=p/security-audit

semgrep \
    --config=auto \
    --json \
    --output="$OUTPUT" \
    "$TARGET"

echo "Semgrep scan complete. Results saved to $OUTPUT"
