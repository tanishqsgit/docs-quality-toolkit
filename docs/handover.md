# Maintain the documentation checker

## Audience and scope

This guide is for a contributor maintaining `check_docs.py`. The tool reads local
Markdown files; it does not edit them or send content to a service.

## Add or change a check

1. Define the reader problem and an example that should fail.
2. Add a focused regression case in `tests/test_check_docs.py`.
3. Add the check in `check_file`, with a rule name and actionable message.
4. Run `python -m unittest discover -s tests -v`.
5. Run `python check_docs.py .` and `python check_docs.py examples --require-metadata`.
6. Update the README's supported checks and limitations.

Keep terminology suggestions advisory unless the team has explicitly adopted the
rule. Check code identifiers before replacing wording.

## Integrate into a publishing workflow

The included `.github/workflows/docs.yml` is a CI example. It requires read-only
repository access and no secrets. Place the check before the publishing step and
require a writer's approval independently. A successful automated run does not approve publication.

## Demonstrate the tool

Run the clean example, temporarily change its link to a nonexistent file, and rerun
the check. Show the line diagnostic and nonzero exit code. Restore the link and
show a passing run. Explain why the tool cannot check technical accuracy.

## Verification record

See [verification](verification.md) for executed checks. The tests use temporary
files and do not modify product data. Human review and product testing remain separate.
