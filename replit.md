# Workspace

## Overview

pnpm workspace monorepo using TypeScript, plus the **VIT Sports Intelligence Network** — a Python/FastAPI sports prediction platform.

## Stack

### TypeScript Monorepo
- **Monorepo tool**: pnpm workspaces
- **Node.js version**: 24
- **Package manager**: pnpm
- **TypeScript version**: 5.9
- **API framework**: Express 5
- **Database**: PostgreSQL + Drizzle ORM
- **Validation**: Zod (`zod/v4`), `drizzle-zod`
- **API codegen**: Orval (from OpenAPI spec)
- **Build**: esbuild (CJS bundle)

### VIT Sports Intelligence Network (Python)
- **Location**: `vit-sports-intelligence/`
- **Backend**: FastAPI (Python 3.11), SQLAlchemy async
- **Frontend**: React 19 + Vite (JSX)
- **ML Engine**: 12-model ensemble for football predictions
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Services**: Telegram alerts, Odds API, Football Data API, AI insights (Gemini/Claude/Grok), CLV tracking, bankroll management
- **Status**: Extracted, organized, security-cleaned, dependency-pinned, and backend/frontend smoke-tested. Full gap analysis available at `vit-sports-intelligence/GAP_ANALYSIS.md`.

## Key Commands

- `pnpm run typecheck` — full typecheck across all packages
- `pnpm run build` — typecheck + build all packages
- `pnpm --filter @workspace/api-spec run codegen` — regenerate API hooks and Zod schemas from OpenAPI spec
- `pnpm --filter @workspace/db run push` — push DB schema changes (dev only)
- `pnpm --filter @workspace/api-server run dev` — run API server locally

## VIT Commands

- `python -m pip install -r vit-sports-intelligence/requirements.txt` — install backend dependencies
- `vit-sports-intelligence/scripts/start_backend.sh` — start FastAPI backend from inside the VIT app folder
- `vit-sports-intelligence/scripts/start_frontend.sh` — start Vite frontend from inside the VIT app folder
- `vit-sports-intelligence/scripts/start_fullstack.sh` — start backend and frontend together for local development

## VIT Application Structure

```
vit-sports-intelligence/
  main.py                 — FastAPI entry point
  requirements.txt        — pinned Python dependencies
  .env.example            — safe template for secrets and runtime config
  README.md               — setup, admin key, and Colab training instructions
  GAP_ANALYSIS.md         — gap analysis, fixed items, and remaining production work
  colab/                  — Colab training script for real model weights
  scripts/                — local startup scripts
  alembic.ini             — database migration config
  alembic/                — migration scripts
  app/
    config.py             — application configuration
    api/routes/           — API route handlers (predict, admin, analytics, training, odds, ai)
    api/middleware/        — auth and logging middleware
    core/dependencies.py  — dependency injection (orchestrator, data loader, alerts)
    db/                   — database models, repositories, connection
    pipelines/            — data loading pipeline
    schemas/              — Pydantic request/response schemas
    services/             — business logic (CLV, bankroll, alerts, AI, scraping, etc.)
    tasks/                — Celery background tasks
    worker.py             — Celery worker config
  services/ml_service/    — ML model orchestrator and 12-model ensemble
  frontend/               — React UI (dashboard, analytics, training, admin)
  data/                   — training data and uploaded historical match JSON
```

## VIT Security Notes

- Runtime admin authentication uses `API_KEY` from environment/secrets and the frontend sends it with the `x-api-key` header.
- The committed frontend `.env` was removed; `.env`, databases, generated model weights, frontend builds, and dependency folders are ignored.
- Admin > API Key Management updates Football Data, Odds API, Telegram, Gemini, Claude, Grok/xAI, and the admin key without code changes.
- Real ML weights are not committed. Generate them with `colab/train_real_match_models.py` and upload the resulting `vit_models.zip` in the admin panel.
