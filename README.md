# LaunchPulse

LaunchPulse is a FastAPI service that stores rocket launches in Postgres and pushes live updates over Server-Sent Events (SSE).

**Stack:** FastAPI · Postgres 17 · Docker Compose · SSE · pytest · GitHub Actions

## Quick start

1. Copy the example below into a `.env` file in the project root (Docker Compose reads these for Postgres):

```env
POSTGRES_USER=launchpulse
POSTGRES_PASSWORD=launchpulse
POSTGRES_DB=launchpulse
```

2. Start the stack:

```bash
docker compose up --build
```

3. Open the API at [http://localhost:8000](http://localhost:8000)  
   Interactive docs: [http://localhost:8000/docs](http://localhost:8000/docs)

Postgres is also exposed on host port `5433` if you want to inspect it with a local client.

## API

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check |
| `GET` | `/launches` | List all launches |
| `GET` | `/launches/{id}` | Get one launch by id |
| `POST` | `/launches/create` | Create a launch |
| `PUT` | `/launches/update` | Update a launch |
| `DELETE` | `/launches/delete/{id}` | Delete a launch |
| `GET` | `/alerts/stream` | Live SSE stream of launch create events |

A small demo page for the stream lives at `/static/alerts.html`.

## Project layout

```
app/           # SSE broadcaster and alert routes
db/            # SQL schema and seed scripts
static/        # Static demo pages
tests/         # pytest
main.py        # FastAPI app and launch CRUD routes
docker-compose.yml
Dockerfile
```

## Development

With the same `.env` and Compose stack running:

```bash
pytest
```

CI runs these checks on every push via GitHub Actions.