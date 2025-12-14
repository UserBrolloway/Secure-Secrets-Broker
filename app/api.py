from fastapi import APIRouter, Depends, HTTPException, Header
from app.schemas import IssueRequest, IssueResponse, RevokeRequest, AuditEventOut
from app.database import SessionLocal
from app.models import Credential, CredentialStatus, AuditEvent
from app.vault_client import VaultClient
from app.audit import record_audit
from app.config import settings
from datetime import datetime, timedelta

router = APIRouter()
vault = VaultClient(settings.vault_addr, settings.vault_token)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def require_admin(x_api_key: str = Header(None)):
    if x_api_key != settings.admin_api_key:
        raise HTTPException(status_code=401, detail="Unauthorized")

@router.post("/v1/issue", response_model=IssueResponse)
def issue(req: IssueRequest, db=Depends(get_db)):
    mount_path = "database"
    vault_resp = vault.issue_database_credential(mount_path, req.role, req.ttl_seconds)
    expires_at = datetime.utcnow() + timedelta(seconds=vault_resp.get("lease_duration", req.ttl_seconds))
    cred = Credential(
        service=req.service,
        role=req.role,
        vault_path=f"{mount_path}/{req.role}",
        expires_at=expires_at,
        status=CredentialStatus.active,
        metadata=""
    )
    db.add(cred)
    db.commit()
    db.refresh(cred)
    record_audit(actor="system", action="issue", target=str(cred.id), metadata=f"role={req.role}")
    return IssueResponse(
        credential_id=cred.id,
        username=vault_resp["username"],
        password=vault_resp["password"],
        expires_at=expires_at
    )

@router.post("/v1/revoke")
def revoke(req: RevokeRequest, db=Depends(get_db)):
    cred = db.query(Credential).filter(Credential.id == req.credential_id).first()
    if not cred:
        raise HTTPException(status_code=404, detail="Credential not found")
    success = vault.revoke_credential(lease_id="")
    if success:
        cred.status = CredentialStatus.revoked
        db.add(cred)
        db.commit()
        record_audit(actor="system", action="revoke", target=str(cred.id))
        return {"status": "revoked"}
    raise HTTPException(status_code=500, detail="Failed to revoke")

@router.get("/v1/audit", response_model=list[AuditEventOut])
def get_audit(limit: int = 50, x_api_key: str = Header(None)):
    require_admin(x_api_key)
    db = SessionLocal()
    try:
        evs = db.query(AuditEvent).order_by(AuditEvent.timestamp.desc()).limit(limit).all()
        return [
            AuditEventOut(
                id=e.id, actor=e.actor, action=e.action, target=e.target,
                timestamp=e.timestamp, metadata=e.metadata
            ) for e in evs
        ]
    finally:
        db.close()
