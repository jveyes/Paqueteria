# ========================================
# PAQUETES EL CLUB v3.1 - Modelo de Logs de Actividad de Usuario
# ========================================

from sqlalchemy import Column, String, Text, DateTime, Enum, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
import uuid
from datetime import datetime

from ..database.database import Base
from ..utils.datetime_utils import get_colombia_now
from ..config import settings

class ActivityType(str, enum.Enum):
    """Tipos de actividad del usuario"""
    LOGIN = "login"
    LOGOUT = "logout"
    PROFILE_UPDATE = "profile_update"
    PASSWORD_CHANGE = "password_change"
    PACKAGE_CREATE = "package_create"
    PACKAGE_UPDATE = "package_update"
    PACKAGE_DELETE = "package_delete"
    FILE_UPLOAD = "file_upload"
    FILE_DELETE = "file_delete"
    USER_CREATE = "user_create"
    USER_UPDATE = "user_update"
    USER_DELETE = "user_delete"
    ROLE_CHANGE = "role_change"
    STATUS_CHANGE = "status_change"

class UserActivityLog(Base):
    """Modelo de logs de actividad de usuario"""
    __tablename__ = "user_activity_logs"
    
    # Campo ID
    if settings.database_url.startswith("sqlite"):
        id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
        user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    else:
        id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    activity_type = Column(Enum(ActivityType), nullable=False)
    description = Column(Text, nullable=False)
    ip_address = Column(String(45), nullable=True)  # IPv6 compatible
    user_agent = Column(String(500), nullable=True)
    activity_metadata = Column(JSON, default=dict)  # Datos adicionales en formato JSON
    
    # Timestamps
    created_at = Column(DateTime, default=get_colombia_now, nullable=False)
    
    # Relaciones
    user = relationship("User", back_populates="activity_logs")
    
    def __repr__(self):
        return f"<UserActivityLog {self.user_id} - {self.activity_type} - {self.created_at}>"
