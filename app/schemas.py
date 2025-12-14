from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class IssueRequest(BaseModel):
    service: str
    role: str
    ttl_seconds: Optional[int] = 3600

class IssueResponse(BaseModel):
    credential_id: int
    username: str
    password: str
    expires_at: Optional[datetime]

class RevokeRequest(BaseModel):
    credential_id: int

class AuditEventOut(BaseModel):
    id: int
    actor: str
    action: str
    target: str
    timestamp: datetime
    metadata: Optional[str]
