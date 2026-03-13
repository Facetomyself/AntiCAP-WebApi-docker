# AntiCAP-WebApi Docker Fork

A Docker-oriented fork of AntiCAP-WebApi that selectively tracks useful upstream changes while keeping a lightweight single-service deployment model.

## What this fork focuses on
- reproducible Docker deployment
- explicit environment-based secrets
- safer authentication defaults
- local health check endpoint
- local Swagger assets instead of external CDN dependency
- preserving a lightweight single-service runtime

## Current baseline
- listens on container port `8000`
- host mapping example: `6688:8000`
- health endpoint: `GET /health`
- Swagger docs: `GET /docs`
- static Swagger assets served from `/swagger/*`

## Required environment variables
Create a `.env` file or provide environment variables:

```env
DEFAULT_USERNAME=admin
DEFAULT_PASSWORD=change-me-now
SECRET_KEY=replace-with-a-long-random-random-string
```

### Notes
- `SECRET_KEY` is required and must stay stable across restarts, otherwise JWT tokens become invalid.
- This fork does **not** allow silent fallback to weak default credentials anymore.
- This fork intentionally keeps env-based single-user auth and does not currently adopt upstream's database / billing / registration-code stack.

## Quick start
```bash
docker compose up -d --build
```

Then open:
- App: <http://localhost:6688/>
- Docs: <http://localhost:6688/docs>
- Health: <http://localhost:6688/health>

## API notes
Login first via `POST /api/login`, then use the returned Bearer token for protected routes.

## Upstream adaptation status
This fork has selectively aligned with newer upstream pieces where they help deployment quality:
- newer `AntiCAP` baseline
- refreshed Python dependency pins
- vendored local Swagger UI assets

It intentionally does **not** fully absorb the newer upstream database/user/billing architecture yet.

## Why this fork diverges from upstream
Upstream has moved toward a broader application shape (database / user system / billing / admin UI changes). This fork keeps a smaller Docker-first surface and only absorbs upstream pieces that fit that model.
