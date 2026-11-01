---
id: 0007
title: Commit Each Small Change
stage: general
date: 2026-10-26
surface: agent
model: GPT-6
feature: none
branch: harden/backend-focused
user: cr33p1ngp4ck3t
command: split backend hardening history
labels: ["git", "focused-commits", "regression-tests"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - history/prompts/general/0007-commit-each-small-change.general.prompt.md
tests:
  - 27 offline tests pass with 93% source coverage
  - Ruff and pip check pass
  - Reviewed source equivalence and original branch preservation pass
---

## Prompt

make sure all small changes get commit

## Response

Reconstructed the existing hardening patch on a separate branch as focused
commits. Each behavior change includes its proving regression tests; operational
and documentation files are separated where they are independently reviewable.

## Outcome

The original published branch remains intact. The new history preserves the
reviewed product behavior and all original tests, adding two client-injection
checks needed to verify the independent slices. Commit count alone does not
establish payout impact.
