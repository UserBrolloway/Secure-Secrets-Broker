# Secure Secrets Broker (MVP)

A beginner-friendly Secure Secrets Broker MVP built with FastAPI that integrates with HashiCorp Vault (dev) and Postgres.

## Quick steps
1. Create the repository and paste files (see repo layout).
2. Copy `.env.example` to `.env`.
3. Run `docker-compose up --build`.
4. Visit `http://localhost:8000/docs` to see the API documentation.
5. Use the CLI inside the app container or the SDK to request credentials.
6. Run tests with `docker-compose exec app pytest -q`.

## Files
See the repo layout in the project root for file responsibilities.

## Notes
This is an MVP for learning and local testing. Production requires Vault AppRole, lease tracking, RBAC, metrics, and secure deployment.
