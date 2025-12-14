from app.vault_client import VaultClient

def test_vault_client_mock():
    vc = VaultClient("http://invalid:8200", "token")
    resp = vc.issue_database_credential("database", "readonly", 3600)
    assert "username" in resp and "password" in resp
