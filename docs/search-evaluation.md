# Plan a documentation search evaluation

This is a test plan, not an implemented RAG system. No embeddings, chatbot, or
search-quality benchmark is claimed.

## Structure content for retrieval

Keep one task per topic. Give it a descriptive heading, prerequisites, expected
results, a product version, and stable links. Keep warnings with the affected step.
Separate procedures from reference tables so retrieved chunks retain their purpose.

## Suggested test cases

| User question | Expected source or behavior | Failure to watch for |
| --- | --- | --- |
| How do I run the docs checker? | README quickstart or examples/quickstart.md | Invented dependencies |
| Does a passing check mean the procedure is accurate? | README boundaries and review checklist | Unqualified yes |
| Which fields are required for metadata? | README checks table | Invented required fields |
| Does the checker validate web links? | README boundaries | Claiming network verification |
| How do I recover a forgotten Study Studio password? | Outside this corpus; abstain | Invented reset steps |

## Record actual results

For each query, record retrieved topic IDs, the answer, source support, completeness,
and harmful omissions. Score support and completeness separately as 0 (absent),
1 (partial), or 2 (complete). Treat an invented command as a failed accuracy gate
regardless of the average score. A writer reviews all answers.

Results template: `query | retrieved sources | answer | support | completeness |
unsupported claims | content gap | reviewer | date`.

No results have been collected. After a real run, distinguish a retrieval failure
from missing or outdated documentation before changing prompts.
