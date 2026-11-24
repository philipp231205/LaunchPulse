# LaunchPulse

[![CI](https://github.com/philipp231205/LaunchPulse/actions/workflows/ci.yml/badge.svg)](https://github.com/philipp231205/LaunchPulse/actions/workflows/ci.yml)

**Live API:** [launchpulse-4dzs.onrender.com/docs](https://launchpulse-4dzs.onrender.com/docs)

LaunchPulse is a REST API for rocket launches. It stores organisations, launch sites, launchpads, vehicles and launches in Postgres. You can filter the data with query parameters, and new launches are pushed live to subscribers over Server-Sent Events (SSE).

**Stack:** FastAPI · PostgreSQL 17 · psycopg 3 · Docker Compose · SSE · pytest · GitHub Actions · Render + Neon

> The live instance runs on Render's free tier, so the first request after a quiet period can take about a minute while it wakes up.

## Features

- Full CRUD for five related tables with foreign keys
- Filtering and pagination on every list endpoint
- Consistent error handling: `404` unknown id or reference, `422` invalid input, `409` deleting a row that is still referenced
- Live launch alerts over SSE, with a small demo page
- 45 pytest tests against a real Postgres database, run on every push by GitHub Actions
- Dockerised, and deployed on Render with Neon Postgres

## Data model

```
organisations ──< launchpads >── locations
      │               │
      ├──< vehicles   │
      │       │       │
      └──< launches >─┘
```

| Table | Fields |
|-------|--------|
| `organisations` | name, country, type, administrator, website |
| `locations` | name, country, region |
| `launchpads` | name, longitude, latitude, status, organisation_id, location_id |
| `vehicles` | name, family, height_m, diameter_m, mass_kg, payload_leo/gto/sso_kg, stages, first_flight, thrust_kn, status, organisation_id |
| `launches` | date, status, webcast_url, mission, payload, vehicle_id, launchpad_id, organisation_id |

The full schema is in [`db/schema.sql`](db/schema.sql).

## API

Every resource has the same five endpoints:

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/{resource}` | List rows (supports filters, `limit`, `offset`) |
| `GET` | `/{resource}/{id}` | Get one row |
| `POST` | `/{resource}` | Create a row, returns `201` |
| `PUT` | `/{resource}/{id}` | Update a row, returns the updated row |
| `DELETE` | `/{resource}/{id}` | Delete a row, returns `204` |

Resources: `organisations`, `locations`, `launchpads`, `vehicles`, `launches`.

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check |
| `GET` | `/alerts/stream` | SSE stream of newly created launches |

A demo page for the stream is at `/static/alerts.html`.

### Filters

All list endpoints accept `limit` (1–200, default 50) and `offset` (default 0). Launches are ordered by date, and everything else by name.

| Resource | Filters |
|----------|---------|
| `organisations` | `country`, `type` |
| `locations` | `country` |
| `launchpads` | `organisation_id`, `location_id`, `status` |
| `vehicles` | `organisation_id`, `status`, `family` |
| `launches` | `status`, `organisation_id`, `launchpad_id`, `vehicle_id`, `from_date`, `to_date` |

Examples:

```
GET /launches?organisation_id=4&from_date=2026-11-01&to_date=2026-12-31
GET /vehicles?status=Active&limit=10
```

### Errors

| Status | When |
|--------|------|
| `404` | The id doesn't exist, or a referenced id (e.g. `organisation_id`) doesn't exist |
| `409` | Deleting a row that other rows still reference |
| `422` | A required field is missing or a parameter is invalid |

## Run it locally

Requires Docker Desktop.

1. Create a `.env` file in the project root:

```env
POSTGRES_USER=launchpulse
POSTGRES_PASSWORD=launchpulse
POSTGRES_DB=launchpulse
DATABASE_URL=postgresql://launchpulse:launchpulse@localhost:5433/launchpulse
TEST_DATABASE_URL=postgresql://launchpulse:launchpulse@localhost:5433/launchpulse_test
```

2. Start the stack:

```powershell
docker compose up --build
```

3. Open [http://localhost:8000/docs](http://localhost:8000/docs).

Postgres is exposed on host port `5433`.

## Tests

The tests run against a separate `launchpulse_test` database. Every table is truncated before each test, so tests never depend on each other.

Create the test database once:

```powershell
docker compose exec db createdb -U launchpulse launchpulse_test
Get-Content db\schema.sql | docker compose exec -T db psql -U launchpulse -d launchpulse_test
```

Run the suite:

```powershell
pytest
```

GitHub Actions runs the same suite on every push to `master`, against a fresh Postgres service container.

## Project layout

```
app/
  routes/        # One router per resource, plus the SSE alerts route
  broadcaster.py # Fans new launches out to SSE subscribers
  db.py          # Postgres connection
models/          # Pydantic request models
db/schema.sql    # Database schema
static/          # SSE demo page
tests/           # pytest suite (conftest has fixtures and helpers)
main.py          # FastAPI app
Dockerfile
docker-compose.yml
.github/workflows/ci.yml
```

## Roadmap

- Use LaunchPulse as the data source for [rocket-launch.space](https://rocket-launch.space)
- Import launch data automatically from Launch Library 2
