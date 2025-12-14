import logging
import hvac
from typing import Dict, Any

logger = logging.getLogger(__name__)

class VaultClient:
    def __init__(self, addr: str, token: str):
        self.addr = addr
        self.token = token
        try:
            self.client = hvac.Client(url=addr, token=token)
            if not self.client.is_authenticated():
                logger.warning("Vault client not authenticated; falling back to mock mode")
                self.client = None
        except Exception:
            logger.exception("Failed to initialize Vault client; falling back to mock mode")
            self.client = None

    def issue_database_credential(self, mount_path: str, role: str, ttl: int) -> Dict[str, Any]:
        if self.client:
            try:
                resp = self.client.secrets.database.generate_credentials(name=role, mount_point=mount_path)
                return {
                    "username": resp["data"]["username"],
                    "password": resp["data"]["password"],
                    "lease_duration": resp.get("lease_duration")
                }
            except Exception:
                logger.exception("Vault DB credential generation failed; falling back to mock")
        return {
            "username": f"{role}_user",
            "password": "mocked-password",
            "lease_duration": ttl
        }

    def revoke_credential(self, lease_id: str) -> bool:
        if self.client:
            try:
                self.client.sys.revoke(lease_id)
                return True
            except Exception:
                logger.exception("Failed to revoke lease")
                return False
        return True
