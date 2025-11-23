## Purpose

This file gives concise, actionable guidance for AI coding agents working in this repository so they can be immediately productive.

## Quick Project Summary

- **Language & runtime:** Python (CI uses Python 3.11).
- **Primary purpose:** Example client for calling 智谱/GLM-style model APIs (see `main.py`).
- **Key components:** `api/` (HTTP client + helpers), `config/` (settings), `tests/` (empty test surface), `Dockerfile`, `.github/workflows/ci.yml` (CI uses `make`).

## Files you should read first

- `main.py` — example runner that constructs a `messages` payload and calls `APIClient.post_data`.
- `api/client.py` — central HTTP client. Use this for all new API calls; it implements a `requests.Session` with retries.
- `api/__init__.py` — exports `APIClient` but has an import-time side effect (`print("API package init!")`). Avoid importing the package root in tests if you want silence.
- `api/utils.py` — logging helpers (use `logger` and `log_request`).
- `config/settings.py` — contains `API_BASE_URL` and `API_KEY` (currently plaintext in repo — treat as a secret).
- `Makefile` and `.github/workflows/ci.yml` — CI steps: `make install`, `make lint`, `make test`.

## Conventions & patterns (concrete)

- **HTTP client usage:** prefer `APIClient` instance methods: `get_data(endpoint, params=None)` and `post_data(endpoint, data)`. Endpoints in this project are appended to `API_BASE_URL` (no leading host in calls).

- **Retry behavior:** `api/client.py` creates a `requests.Session` with `Retry(total=3, backoff_factor=1, status_forcelist=[500,502,503,504])`. Do not add duplicate retry wrappers; adjust `Retry` only in `APIClient._create_session`.

- **Payload shape:** follow `main.py` example — models expect JSON with keys like `model` and `messages` (a list of `{role, content}` objects). Example payload:

```
{"model": "glm-4-flash", "messages": [{"role":"system","content":"..."}, {"role":"user","content":"..."}]}
```

- **Logging:** use `api.utils.logger` and call `log_request(response)` when you want standardized request logs.

- **Import side-effects:** `api/__init__.py` prints at import time. To avoid console noise in tests, import `APIClient` with `from api.client import APIClient` instead of `import api` or `from api import APIClient`.

## Developer workflows / commands

- Install deps: `pip install -r requirements.txt` or `make install` (CI uses `make install`).
- Run the example: `python main.py` (this runs the example against `API_BASE_URL` with configured `API_KEY`).
- Run tests: `pytest -v` or `make test` (Makefile runs `pytest -v --cov`).
- Linting in CI: `make lint` (Makefile runs `ruff` and `mypy src` — note: the project doesn't currently use `src/`, so `mypy` may be a stale entry).

## Project-specific gotchas

- **Plaintext API key:** `config/settings.py` currently contains a literal `API_KEY`. Treat it as secret. Preferred pattern: use environment variables (e.g., `os.environ['API_KEY']`) and `.env` for local dev. Do not commit real keys.

- **Makefile ≠ reality:** `Makefile` refers to `mypy src` and formatting commands with inconsistent indentation. CI calls `make lint` and `make test` — expect lint or mypy issues if you change structure. When adding typed code, either place it under `src/` or update the Makefile/mypy config.

- **Tests are minimal:** `tests/` is empty. Add focused tests next to new features and keep them small.

## How to add a new API call (recommended minimal steps)

1. Prefer reusing `APIClient.post_data` / `get_data` from `api/client.py`.
2. Add a small wrapper method in `APIClient` if the call is used in multiple places.
3. Add a unit test in `tests/` that imports `from api.client import APIClient` (avoid `api` root import to prevent the print side-effect). Mock network calls (e.g., with `responses` or `requests-mock`).
4. Run `pytest -v` and `ruff check .` locally. Update CI only if you must change `Makefile` behavior.

## Example snippets (copy-paste)

- Create client and post:

```
from api.client import APIClient

client = APIClient()
resp = client.post_data('/api/paas/v4/chat/completions', data={
    "model": "glm-4-flash",
    "messages": [{"role":"system","content":"你是一位温柔的朋友"}, {"role":"user","content":"你好"}]
})
print(resp['choices'][0]['message'])
```

## Where to look when debugging

- Network behavior: `api/client.py` and `api/utils.py`.
- Config & secrets: `config/settings.py`.
- CI failures: `.github/workflows/ci.yml` and `Makefile` targets.

---

If anything here is unclear or you'd like additional examples (more unit-test examples, a suggested `.env` pattern, or a small patch to remove the `print()` side-effect), tell me which area to expand and I will update this file.
