import click
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "http://app:8000")

@click.group()
def cli():
    pass

@cli.command()
@click.option("--service", required=True)
@click.option("--role", required=True)
@click.option("--ttl", default=3600)
def issue(service, role, ttl):
    payload = {"service": service, "role": role, "ttl_seconds": ttl}
    resp = requests.post(f"{API_URL}/v1/issue", json=payload)
    resp.raise_for_status()
    print(resp.json())

@cli.command()
@click.option("--credential-id", required=True, type=int)
def revoke(credential_id):
    payload = {"credential_id": credential_id}
    resp = requests.post(f"{API_URL}/v1/revoke", json=payload)
    resp.raise_for_status()
    print(resp.json())

if __name__ == "__main__":
    cli()
