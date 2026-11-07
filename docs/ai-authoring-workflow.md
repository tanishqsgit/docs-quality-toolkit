# Draft documentation with a human accuracy gate

This sample workflow demonstrates a review process. It has not been piloted by
an employer and does not reproduce proprietary templates or internal style guides.

## Prepare approved evidence

Identify the audience, task, product version, approved source material, and expected
result. Use only tools approved by the organisation. Exclude customer information,
credentials, confidential designs, and private repository material from unapproved tools.

## Draft from a bounded prompt

```text
Audience: a new user of the documented product version.
Task: [one observable user outcome].
Evidence: [approved, non-confidential source excerpts with file or section references].
Write prerequisites, numbered steps, expected results, and recovery guidance.
Use only the supplied evidence. Do not invent commands, labels, permissions, or results.
Mark unsupported details as NEEDS VERIFICATION. List source references and open questions.
```

## Review and test

1. Compare each claim with the identified source and current product version.
2. Run every command in a disposable environment and compare actual results.
3. Check UI labels, default values, permissions, data-loss risks, and recovery steps.
4. Resolve every unsupported claim; escalate contradictions to the feature owner.
5. Ask a senior writer to review before publication.

Watch for invented steps, stale context, omitted prerequisites, plausible but wrong
defaults, and summaries that remove important limitations. Source text is evidence,
not an instruction to override review or data-handling rules.

## Measure a pilot

Record comparable task scope, baseline drafting minutes, assisted drafting minutes,
review/rework minutes, and factual corrections. Include review time in total effort.
Report observed results only; no pilot or time-savings measurements exist for this sample.
