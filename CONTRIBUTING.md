# Contributing

Use Python 3.13 and keep each behavior change with the tests that prove it.

Commit completed slices regularly. Keep each feature or fix in its own focused
commit or small PR, including the regression tests that pin its behavior. Keep
unrelated formatting and refactors in separate commits so each change can be
reviewed and understood on its own.

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements-lock.txt -r requirements-dev-lock.txt
.venv/Scripts/python -m ruff check src tests
.venv/Scripts/python -m pytest tests -v
```

On macOS or Linux, use `.venv/bin/python`. Tests must run without a Gemini key or network access. Keep live Gemini checks as explicit demos, outside the `tests/` directory.

Regenerate dependency locks from a clean Python 3.13 environment:

```bash
python -m pip install -r requirements.txt
python -m pip freeze --exclude-editable > requirements-lock.txt
python -m pip install -r requirements-dev.txt
python -m pip freeze --exclude-editable > requirements-dev-lock.txt
```

Freeze runtime dependencies before installing development tools. The development lock
can contain the complete environment; its runtime pins must match the runtime lock.
Node.js 22 is needed for the browser-rendering self-check; CI installs it explicitly.
