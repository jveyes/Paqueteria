# ========================================
# PAQUETES EL CLUB v3.1 - Modelo de Cliente
# ========================================

from sqlalchemy import Column, String, Index
from sqlalchemy.orm import relationship

from .base import BaseModel
from ..database.database import Base

class Customer(BaseModel, Base):
    """Modelo de cliente simplificado"""
    __tablename__ = "customers"
    
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    tracking_number = Column(String(50), unique=True, nullable=False, index=True)
    
    # Relaciones
    packages = relationship("Package", back_populates="customer")
    
    # Índices
    __table_args__ = (
        Index('idx_customer_phone', 'phone'),
        Index('idx_customer_name', 'name'),
    )
    
    def __repr__(self):
        return f"<Customer {self.name} - {self.tracking_number}>"
# Commit 45 - 2024-02-11
# Change: 1757423581
# Commit 61 - 2024-02-25
# Change: 1757423582
# Commit 72 - 2024-03-07
# Change: 1757423583
# Commit 96 - 2024-03-29
# Change: 1757423584
# Commit 111 - 2024-04-11
# Change: 1757423584
# Commit 113 - 2024-04-13
# Change: 1757423585
# Commit 121 - 2024-04-20
# Change: 1757423585
# Commit 127 - 2024-04-26
# Change: 1757423585
# Commit 137 - 2024-05-05
# Change: 1757423586
# Commit 156 - 2024-05-23
# Change: 1757423587
# Commit 157 - 2024-05-23
# Change: 1757423587
# Commit 163 - 2024-05-29
# Change: 1757423587
# Commit 170 - 2024-06-04
# Change: 1757423587
# Commit 192 - 2024-06-25
# Change: 1757423588
# Commit 243 - 2024-08-10
# Change: 1757423591
# Commit 247 - 2024-08-14
# Change: 1757423591
# Commit 248 - 2024-08-15
# Change: 1757423591
# Commit 256 - 2024-08-22
# Change: 1757423592
# Commit 258 - 2024-08-24
# Change: 1757423592
# Commit 272 - 2024-09-06
# Change: 1757423592
# Commit 292 - 2024-09-24
# Change: 1757423593
# Commit 300 - 2024-10-02
# Change: 1757423594
# Commit 306 - 2024-10-07
# Change: 1757423594
# Commit 308 - 2024-10-09
# Change: 1757423594
# Commit 312 - 2024-10-13
# Change: 1757423594
# Commit 318 - 2024-10-18
# Change: 1757423595
# Commit 338 - 2024-11-05
# Change: 1757423595
# Commit 344 - 2024-11-11
# Change: 1757423596
# Commit 355 - 2024-11-21
# Change: 1757423596
# Commit 365 - 2024-11-30
# Change: 1757423597
# Commit 388 - 2024-12-21
# Change: 1757423598
