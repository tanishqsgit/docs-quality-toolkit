---
title: Check a documentation folder
audience: Documentation contributors
status: sample
---
# Check a documentation folder

Use this procedure to find missing local link targets before requesting a review.

## Before you begin

Install Python 3.10 or later. Open a terminal in the repository root.
The checker uses the standard library and needs no API key or network access.

## Run the check

1. Run `python check_docs.py examples --require-metadata`.
2. Confirm the output reports one Markdown file and zero issues.
3. Run `python check_docs.py .` to check the rest of the repository.

## Fix a missing link

If a diagnostic reports `link`, open the file at the reported line. Correct the relative
path or add the missing file, then repeat the check. Exit code `0` means the enabled
checks passed; it does not establish technical accuracy.

## Next step

Ask a reviewer to follow each product procedure. Use `docs/review-checklist.md`
in the repository root.
