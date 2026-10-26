# Focused backend hardening history

Goal: replace the mixed hardening commit with independently checked slices on
`harden/backend-focused`, based on `e2d0967`. Preserve `harden/backend-review` at
`29fd245`; never reset or force-push it. Product behavior and file contents must match that reviewed branch after
normalizing line endings and terminal blank lines. Tests may be introduced incrementally, but all existing
tests must be present at the end.

For each code slice: introduce its existing regression tests, prove the new test
fails against the preceding implementation where applicable, apply the reviewed
implementation, run every test available at that point, check whitespace, and
commit only that slice. Reuse the installed offline environment. No live API calls.

Commit boundaries, in dependency order:

1. Offline serialization and graph baseline tests, discovery, dev dependencies.
2. Request-scoped Gemini client and provider error regression.
3. Overlapping SDK credential lock and concurrency regression.
4. Client injection throughout sequential agents and orchestrator regression.
5. Contradiction client injection and fake-client check.
6. Synthesis client injection and fake-client check.
7. API credential isolation and request-key regression.
8. Graph isolation, retired graph endpoint, compatibility regression.
9. JSON-object input guard and regression.
10. Pydantic request validation, runtime dependency, field regressions.
11. Environment-key validation and boundary regressions.
12. JSON oversized-body rejection and regression.
13. Health endpoint and regression.
14. Signature response validation and malformed-output regression.
15. Contradiction provider failures and explicit-error regression.
16. Contradiction response validation and malformed-output regression.
17. Synthesis response validation, private degraded fallback, regression.
18. Signature arbitration/degradation metadata and parallel lineage regression.
19. Safe API failures/logging and privacy regression.
20. Strict signature scores and type regression.
21. Strict contradiction flags/scores and type regression.
22. Browser generated-content escaping and executed-JavaScript regression.
23. Accessible synthesis fallback notice and executed-JavaScript regression.
24. Runtime lock, development lock, serverless dependencies, Python runtime.
25. Lint and coverage configuration with corresponding export corrections.
26. Hosted offline test job.
27. Docker packaging with secret/artifact exclusions.
28. Hosted container health job.
29. Dependency update configuration.
30. Onboarding, release notes, implementation plan, and verification records,
    each documentation file in a separate commit.
31. Contribution commit rules and split-history handoff, separately.

Final gates: every original test present; pytest and Ruff pass; product file bytes
match `29fd245`; full-range whitespace check; clean working tree; original branch
ref unchanged. Report the actual commit count and limitations. More commits do
not independently establish payout impact.


Execution result: 23 behavior/client/test slices were committed first, followed
by 21 operational, documentation, and test-layout slices. Every slice passed
the complete offline suite present at that point before its commit. Existing
behavior regressions failed before the corresponding fixes where applicable.
The final suite passes 27 tests with 93% coverage; Ruff and pip check pass.
All original test functions are preserved. Two client-injection regressions
were introduced with their injection slices and retained in the final suite.
Compared with 29fd245, reviewed source ASTs and non-test file contents match
after line-ending normalization. The template omits one trailing blank line.
The original harden/backend-review ref remains unchanged at 29fd245.
