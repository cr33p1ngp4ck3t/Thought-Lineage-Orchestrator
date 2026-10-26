# Changelog

## Unreleased

- Added offline pytest coverage and push/pull-request CI.
- Isolated API keys and model selection to each request.
- Added request validation, structured logging, safe client errors, and `/health`.
- `GET /api/graph` now returns `410 Gone`; callers must use the graph in `POST /api/process` responses.
- Made contradiction detection failures explicit and synthesis fallback visible.
- Escaped model-generated text before rendering it in the browser.
- Added reproducible dependency locks, Dependabot, and a Docker image.
