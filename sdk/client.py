import requests
from typing import Dict
import os

class BrokerClient:
    def __init__(self, base_url: str = None):
        self.base_url = base_url or os.getenv("API_URL", "http://localhost:8000")

    def issue(self, service: str, role: str, ttl_seconds: int = 3600) -> Dict:
        resp = requests.post(f"{self.base_url}/v1/issue", json={
            "service": service, "role": role, "ttl_seconds": ttl_seconds
        })
        resp.raise_for_status()
        return resp.json()

    def revoke(self, credential_id: int) -> Dict:
        resp = requests.post(f"{self.base_url}/v1/revoke", json={"credential_id": credential_id})
        resp.raise_for_status()
        return resp.json()
