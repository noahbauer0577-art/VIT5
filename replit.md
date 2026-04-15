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
- **Status**: Extracted and organized. Full gap analysis available at `vit-sports-intelligence/GAP_ANALYSIS.md`

## Key Commands

- `pnpm run typecheck` — full typecheck across all packages
- `pnpm run build` — typecheck + build all packages
- `pnpm --filter @workspace/api-spec run codegen` — regenerate API hooks and Zod schemas from OpenAPI spec
- `pnpm --filter @workspace/db run push` — push DB schema changes (dev only)
- `pnpm --filter @workspace/api-server run dev` — run API server locally

## VIT Application Structure

```
vit-sports-intelligence/
  main.py                 — FastAPI entry point
  alembic.ini             — Database migration config
  alembic/                — Migration scripts
  app/
    config.py             — Application configuration
    api/routes/           — API route handlers (predict, admin, analytics, training, odds, ai)
    api/middleware/        — Auth & logging middleware
    core/dependencies.py  — Dependency injection (orchestrator, data loader, alerts)
    db/                   — Database models, repositories, connection
    pipelines/            — Data loading pipeline
    schemas/              — Pydantic request/response schemas
    services/             — Business logic (CLV, bankroll, alerts, AI, scraping, etc.)
    tasks/                — Celery background tasks
    worker.py             — Celery worker config
  services/ml_service/    — ML model orchestrator and 12-model ensemble
  frontend/               — React UI (dashboard, analytics, training, admin)
  data/                   — Training data
```

See the `pnpm-workspace` skill for workspace structure, TypeScript setup, and package details.
