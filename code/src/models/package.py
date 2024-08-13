# ========================================
# PAQUETES EL CLUB v3.0 - Modelo de Paquete
# ========================================

from sqlalchemy import Column, String, Text, Numeric, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
from datetime import datetime

from .base import BaseModel
from ..database.database import Base
from .customer import Customer
from .file import File

class PackageStatus(str, enum.Enum):
    """Estados del paquete"""
    ANUNCIADO = "anunciado"
    RECIBIDO = "recibido"
    EN_TRANSITO = "en_transito"
    ENTREGADO = "entregado"
    CANCELADO = "cancelado"

class PackageType(str, enum.Enum):
    """Tipos de paquete"""
    NORMAL = "normal"
    EXTRA_DIMENSIONADO = "extra_dimensionado"

class PackageCondition(str, enum.Enum):
    """Condición del paquete"""
    BUENO = "bueno"
    REGULAR = "regular"
    MALO = "malo"

class Package(BaseModel, Base):
    """Modelo de paquete"""
    __tablename__ = "packages"
    
    tracking_number = Column(String(50), unique=True, nullable=False, index=True)
    customer_name = Column(String(100), nullable=False)
    customer_phone = Column(String(20), nullable=False)
    status = Column(Enum(PackageStatus), default=PackageStatus.ANUNCIADO)
    package_type = Column(Enum(PackageType), default=PackageType.NORMAL)
    package_condition = Column(Enum(PackageCondition), default=PackageCondition.BUENO)
    storage_cost = Column(Numeric(10, 2), default=0)
    delivery_cost = Column(Numeric(10, 2), default=0)
    total_cost = Column(Numeric(10, 2), default=0)
    observations = Column(Text, nullable=True)
    
    # Timestamps específicos
    announced_at = Column(DateTime, nullable=True)
    received_at = Column(DateTime, nullable=True)
    delivered_at = Column(DateTime, nullable=True)
    
    # Relaciones - Solo UUID para PostgreSQL AWS RDS
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=True)
    customer = relationship("Customer", back_populates="packages")
    notifications = relationship("Notification", back_populates="package")
    files = relationship("File", back_populates="package")
    
    def __repr__(self):
        return f"<Package {self.tracking_number} - {self.status}>"
# Commit 1 - 2024-01-01
# Change: 1757423578
# Commit 64 - 2024-02-28
# Change: 1757423582
# Commit 68 - 2024-03-03
# Change: 1757423582
# Commit 76 - 2024-03-10
# Change: 1757423583
# Commit 77 - 2024-03-11
# Change: 1757423583
# Commit 86 - 2024-03-19
# Change: 1757423583
# Commit 90 - 2024-03-23
# Change: 1757423583
# Commit 97 - 2024-03-29
# Change: 1757423584
# Commit 102 - 2024-04-03
# Change: 1757423584
# Commit 118 - 2024-04-18
# Change: 1757423585
# Commit 134 - 2024-05-02
# Change: 1757423586
# Commit 167 - 2024-06-02
# Change: 1757423587
# Commit 169 - 2024-06-03
# Change: 1757423587
# Commit 177 - 2024-06-11
# Change: 1757423588
# Commit 183 - 2024-06-16
# Change: 1757423588
# Commit 190 - 2024-06-23
# Change: 1757423588
# Commit 199 - 2024-07-01
# Change: 1757423589
# Commit 210 - 2024-07-11
# Change: 1757423589
# Commit 211 - 2024-07-12
# Change: 1757423589
# Commit 219 - 2024-07-19
# Change: 1757423590
# Commit 225 - 2024-07-25
# Change: 1757423590
# Commit 230 - 2024-07-29
# Change: 1757423590
# Commit 242 - 2024-08-09
# Change: 1757423591
# Commit 245 - 2024-08-12
# Change: 1757423591
# Commit 246 - 2024-08-13
# Change: 1757423591
