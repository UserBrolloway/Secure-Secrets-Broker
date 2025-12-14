from sqlalchemy import Column, Integer, String, DateTime, Text, Enum
from sqlalchemy.sql import func
from app.database import Base
import enum

class CredentialStatus(str, enum.Enum):
    active = "active"
    revoked = "revoked"
    expired = "expired"

class Credential(Base):
    __tablename__ = "credentials"
    id = Column(Integer, primary_key=True, index=True)
    service = Column(String(128), nullable=False)
    role = Column(String(128), nullable=False)
    vault_path = Column(String(256), nullable=True)
    issued_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
    status = Column(Enum(CredentialStatus), default=CredentialStatus.active)
    metadata = Column(Text, nullable=True)

class AuditEvent(Base):
    __tablename__ = "audit_events"
    id = Column(Integer, primary_key=True, index=True)
    actor = Column(String(128), nullable=False)
    action = Column(String(64), nullable=False)
    target = Column(String(256), nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    metadata = Column(Text, nullable=True)
