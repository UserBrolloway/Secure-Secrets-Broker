from app.database import SessionLocal
from app.models import AuditEvent

def record_audit(actor: str, action: str, target: str = None, metadata: str = None):
    db = SessionLocal()
    try:
        ev = AuditEvent(actor=actor, action=action, target=target or "", metadata=metadata)
        db.add(ev)
        db.commit()
    finally:
        db.close()
