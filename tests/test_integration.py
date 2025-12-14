import requests
import os
import time

API_URL = os.getenv("API_URL", "http://localhost:8000")

def test_issue_and_revoke():
    for _ in range(10):
        try:
            r = requests.get(f"{API_URL}/docs")
            if r.status_code == 200:
                break
        except Exception:
            time.sleep(1)
    payload = {"service": "demo", "role": "readonly", "ttl_seconds": 60}
    r = requests.post(f"{API_URL}/v1/issue", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "credential_id" in data
    cred_id = data["credential_id"]
    r2 = requests.post(f"{API_URL}/v1/revoke", json={"credential_id": cred_id})
    assert r2.status_code == 200
