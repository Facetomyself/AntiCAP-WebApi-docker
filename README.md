# AntiCAP-WebApi Docker Fork

A Docker-oriented fork of AntiCAP-WebApi that selectively tracks useful upstream changes while keeping a lightweight single-service deployment model.

## What this fork focuses on
- reproducible Docker deployment
- explicit environment-based secrets
- safer authentication defaults
- local health check endpoint
- local Swagger assets instead of external CDN dependency
- preserving a lightweight single-service runtime
- keeping the service usable even when upstream AntiCAP has edge-case inference failures

## Current baseline
- listens on container port `8000`
- host mapping example: `6688:8000`
- health endpoint: `GET /health`
- Swagger docs: `GET /docs`
- static Swagger assets served from `/swagger/*`
- JWT login endpoint: `POST /api/login`

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

## What changed in this refresh
This fork was refreshed toward a newer AntiCAP / upstream-style baseline without importing the full upstream database and billing stack.

### Included in this refresh
- upgraded to `AntiCAP==3.3.5`
- refreshed Python dependency pins
- local vendored Swagger UI assets (no external CDN required for docs)
- Docker runtime adjustments for newer AntiCAP model download/cache behavior
- compatibility fix for the similarity endpoint after AntiCAP API drift
- defensive handling for double-rotate edge-case failures

### Intentionally not adopted from upstream
- database-backed users
- registration-code / billing flow
- admin / balance / endpoint-cost stack
- heavier multi-role application shape

## Validation status
The refreshed Docker fork was tested in-container and confirmed working for:
- `GET /health`
- `GET /docs`
- `POST /api/login`
- `GET /api/tokens/verification`
- `GET /api/models`
- `POST /api/ocr`
- `POST /api/math`
- `POST /api/detection/icon`
- `POST /api/detection/text`
- `POST /api/detection/text/order`
- `POST /api/slider/comparison`
- `POST /api/compare/similarity`
- `POST /api/rotate/double/rotate`

## Known behavior / limitations
### Double rotate
`/api/rotate/double/rotate` is functional, including on public real-world sample pairs, but upstream `AntiCAP 3.3.5` still has at least one edge-case crash inside its rotation algorithm for some image pairs.

To keep the API stable, this fork now converts those upstream exceptions into a structured `422 Unprocessable Entity` response instead of a raw `500`.

Example error shape:

```json
{
  "detail": {
    "message": "double rotate failed on this image pair",
    "error": "...upstream exception text...",
    "error_type": "error type name"
  }
}
```

This means:
- successful image pairs still return normal `result` payloads
- problematic image pairs fail in a predictable, client-handleable way

## API notes
Login first via `POST /api/login`, then use the returned Bearer token for protected routes.

## Why this fork diverges from upstream
Upstream has moved toward a broader application shape (database / user system / billing / admin UI changes). This fork keeps a smaller Docker-first surface and only absorbs upstream pieces that fit that model.
