# AI Code Review Assistant

Full-stack app: upload code, get Pylint/Bandit/Radon metrics + an AI-generated
review (bugs, smells, security, refactors) in one dashboard.

## Structure

```
backend/    Flask API (JWT auth, file upload, analysis pipeline, review CRUD)
frontend/   React + Tailwind SPA (Vite)
```

## Backend setup

```bash
cd backend
python -m venv venv && source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                                 # fill in secrets
python app.py                                         # runs on :5000
```

Notes:
- Defaults to a local SQLite file (`dev.db`) so it runs with zero setup.
  Swap `DATABASE_URL` in `.env` for a Postgres URL when you're ready
  (`postgresql://user:pass@host:5432/dbname`), install `psycopg2-binary`
  (already in requirements.txt), and `db.create_all()` will build the schema.
- `pylint`, `bandit`, and `radon` run as subprocesses — make sure they're on
  PATH (they install with `pip install -r requirements.txt`).
- Without `OPENAI_API_KEY` set, the AI review step returns a graceful
  "not configured" placeholder instead of failing the whole pipeline — static
  analysis results still come through.

## Frontend setup

```bash
cd frontend
npm install
npm run dev          # runs on :5173, proxies /api to :5000
```

## What's wired up

- Register / login / JWT auth, "me" + profile update
- Upload a file or paste a snippet → runs Pylint + Bandit + Radon, then an AI
  pass, and stores everything as a `Review` with per-issue `ReviewFinding`s
- Dashboard: list, search by project name, filter by score, delete
- Review detail page: metrics, severity-coded findings list
- Markdown export (`/api/reports/<id>/markdown`)

## Not yet built (from the doc's bonus/optional list)

- GitHub repo URL ingestion (only direct file/snippet upload is wired up —
  `upload_type` already has a `"github"` slot in the schema for this)
- PDF export (ReportLab is in requirements.txt; `routes/report.py` has a
  comment showing where to add it)
- Monaco code editor (Upload page uses a plain textarea for now)
- Multi-language static analysis (Pylint/Bandit/Radon are Python-only; JS/TS
  files currently only go through the AI review step)

## Suggested next steps

If you want to keep building, the natural next steps in doc order are:
GitHub URL ingestion → PDF export → Monaco editor → review history filters
(severity, source) → documentation generator (function/class/module docstrings
via the AI service, same pattern as `openai_service.py`).
