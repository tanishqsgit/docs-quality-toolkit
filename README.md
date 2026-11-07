# Docs Quality Toolkit

A small Python tool for checking Markdown before review. It catches missing local
link targets, missing topic titles, and optional metadata omissions. A configurable
terminology check flags wording for a writer to assess.

**Stack:** Python standard library · Markdown · unittest · GitHub Actions

The toolkit is an AI-assisted portfolio project. Its automated checks run locally
without third-party packages, network access, or API credentials.

## Quickstart

Requires Python 3.10 or later. No third-party packages, credentials, or API calls.

```sh
git clone https://github.com/tanishqsgit/docs-quality-toolkit.git docs-quality-toolkit
cd docs-quality-toolkit
python check_docs.py .
python check_docs.py examples --require-metadata
python -m unittest discover -s tests -v
```

The first command reports how many Markdown files it checked. A clean check exits
with `0`; errors exit with `1`. Invalid command options or configuration exit with `2`.
Follow the [task-based quickstart](examples/quickstart.md) for an example workflow.

## Checks

| Check | Default behavior | What the writer should do |
| --- | --- | --- |
| Topic title | Error if no level-one heading exists | Identify the topic clearly |
| Local links and images | Error if a relative file target is absent or leaves the repository | Correct the path or add the file |
| Metadata | With `--require-metadata`, require `title`, `audience`, and `status` | Supply non-empty front matter fields |
| Terminology | With `--terms terms.json`, report advisory warnings | Assess the preferred wording in context |

```sh
python check_docs.py examples --require-metadata --json
python check_docs.py examples --terms terms.json --strict
```

`--strict` makes terminology warnings fail the run. The sample terminology list is
an independent example. Replace it with your team's approved terminology before
using it as a policy check.

## How it works

The script discovers `.md` files recursively, skips common dependency/build folders,
and inspects prose outside fenced code blocks and inline code. It prints file and
line diagnostics, or structured JSON for another tool to consume.

GitHub Actions runs tests and checks on pushes and pull requests. Copy the script
into another repository to run it there, or pass a local repository folder as `root`.
See the [handover guide](docs/handover.md) before changing the rules.

## Boundaries

- This is a lightweight regex parser, not a complete CommonMark or YAML parser.
- It supports ordinary inline links, images, and reference definitions. Nested
  parentheses, multiline destinations, embedded HTML links, and complex markup need review.
- It checks file existence, not heading anchors, undefined reference usages, redirects,
  website availability, site-root routing, or the contents of linked pages.
- Front matter supports simple one-line fields; metadata dates and values are not validated.
- It does not establish product accuracy, security, accessibility, or readiness to publish.
- A passing check requires a human accuracy review before publication.

## Writing and responsible AI samples

- [AI-assisted authoring workflow](docs/ai-authoring-workflow.md): grounded drafting and human review.
- [Review checklist](docs/review-checklist.md): audience, prerequisites, procedures, and factual checks.
- [Search evaluation plan](docs/search-evaluation.md): retrieval test cases and an unscored results template.

AI assisted the implementation and documentation of this toolkit. Automated test
results are recorded separately from human review. No time savings, search-quality
scores, customer adoption, or unaided authorship are claimed.
