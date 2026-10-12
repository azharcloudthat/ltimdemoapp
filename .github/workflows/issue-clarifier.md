---
description: |
  Reviews newly opened issues for completeness, identifies likely duplicates, and posts a concise maintainer-facing summary with any needed follow-up questions.
on:
  issues:
    types: [opened]
permissions:
  copilot-requests: write
  contents: read
  issues: read
engine:
  id: copilot
  model: gpt-5
safe-outputs:
  add-comment:
timeout-minutes: 10
---

# Issue Clarifier

Analyze issue #${{ github.event.issue.number }} and help maintainers understand and route it quickly. Base every conclusion on the issue, its discussion, and repository context. Do not invent missing details.

## 1. Gather context

1. Read the issue and its comments.
2. Inspect the repository's available labels and issue types.
3. Search open and recent closed issues for the same symptoms, request, error
   messages, affected component, or expected behavior.
4. Consult relevant repository documentation when it clarifies expected behavior
   or contribution requirements.

## 2. Assess completeness

Decide whether the issue contains enough information for meaningful triage.

For a bug, look for reproduction steps, expected and actual behavior, relevant logs or errors, and environment details. 
For a feature or task, look for the problem being solved, desired outcome, and enough scope to understand the request.

If essential details are missing:

- ask only the specific questions needed to proceed
- do not guess a type, priority, or solution

If the issue is clearly spam, gibberish, or a test submission, apply `spam` or `invalid` when available and explain the assessment briefly. Do not perform the remaining triage.