# Secure Secrets Broker (MVP)

A production-oriented Secure Secrets Broker MVP built with FastAPI that integrates with HashiCorp Vault to issue short-lived credentials, record audit events, and provide a CLI and SDK.

## Features (MVP)
- `/v1/issue` to request credentials for a service/role
- `/v1/revoke` to revoke credentials
- `/v1/audit` to view audit events (admin)
- Vault integration with dev fallback
- Postgres metadata and audit storage
- Docker Compose for local dev
- CLI and Python SDK
- Unit and integration test examples
- GitHub Actions CI workflow

## Quickstart (local)
1. Copy files into a new repo.
2. Create `.env` from `.env.example`.
3. Start services:
   ```bash
   docker-compose up --build
