# AI Business Assistant

A multi-tenant AI automation platform for small businesses (restaurants, clinics,
gyms, salons, travel agencies, real estate, coaching institutes). The backend is
fully generic — only the uploaded knowledge base changes per business.

> **Status: Phase 1 of 11 complete — Authentication.**
> See `docs/architecture.md` for the full system design and roadmap.

## Architecture at a glance

- **Backend**: Python 3.12, FastAPI, async SQLAlchemy 2.0, PostgreSQL, Redis
- **AI layer** (Phase 6+): LangGraph orchestration, pluggable LLM providers
  (OpenAI / Gemini / Claude), Qdrant for RAG
- **Pattern**: Layered architecture — Router → Service → Repository, with
  dependency injection wired in `app/api/deps.py`. No layer talks to a layer
  two hops away.
- **Multi-tenancy**: shared tables with `business_id` scoping, hardened with
  Postgres Row-Level Security from Phase 2 onward.

## Phase 1: Authentication

Implements registration, login, JWT access/refresh tokens, and `/auth/me`.

### Run locally

```bash
cd backend
cp .env.example .env
# edit JWT_SECRET_KEY in .env — generate one with:
python -c "import secrets; print(secrets.token_urlsafe(48))"

python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

alembic upgrade head
uvicorn app.main:app --reload
```

Or via Docker Compose (Postgres + Redis + backend):

```bash
docker compose -f docker/docker-compose.yml up --build
```

### Try it

```bash
./scripts/curl_examples_auth.sh
```

Or open `http://localhost:8000/docs` for interactive Swagger UI.

### Run tests

```bash
pytest tests/unit                  # no DB required, runs in ~1s
pytest tests/integration -m integration   # requires Postgres running
```

### Code quality

```bash
ruff check app tests
black --check app tests
mypy app
```

## Project structure

```
backend/app/
├── api/routers/      HTTP endpoints only — no business logic
├── schemas/          Pydantic v2 request/response models
├── models/            SQLAlchemy ORM models
├── repositories/      Persistence queries — no business logic
├── services/           Business logic — no SQL, no HTTP
├── auth/                JWT + password hashing primitives
├── middleware/        Logging, error handling
├── config/             Settings (env-driven), logging config
├── database/          Async session factory, RLS-ready tenant context
└── utils/exceptions.py Custom exception hierarchy
```

See `docs/architecture.md` for the full architecture, ER diagram, API
design, and the remaining 10-phase roadmap (Business CRUD → FAQ →
Knowledge Base → Vector DB → RAG → AI Agent → WhatsApp → Dashboard →
Analytics → Deployment).
