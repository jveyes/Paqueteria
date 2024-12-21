# ========================================
# PAQUETES EL CLUB v3.0 - Router de Clientes
# ========================================

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional

from ..database.database import get_db
from ..models.customer import Customer
from ..schemas.customer import CustomerCreate, CustomerResponse, CustomerUpdate, CustomerSearch
from ..dependencies import get_current_active_user

router = APIRouter()

@router.post("/", response_model=CustomerResponse)
async def create_customer(
    customer_data: CustomerCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Crear nuevo cliente"""
    # Verificar si ya existe un cliente con ese tracking number
    existing_customer = db.query(Customer).filter(
        Customer.tracking_number == customer_data.tracking_number
    ).first()
    
    if existing_customer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un cliente con ese número de tracking"
        )
    
    # Crear cliente
    db_customer = Customer(**customer_data.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    
    return db_customer

@router.get("/", response_model=List[CustomerResponse])
async def list_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Listar clientes con filtros"""
    query = db.query(Customer)
    
    if search:
        query = query.filter(
            or_(
                Customer.name.ilike(f"%{search}%"),
                Customer.phone.ilike(f"%{search}%"),
                Customer.tracking_number.ilike(f"%{search}%")
            )
        )
    
    customers = query.offset(skip).limit(limit).all()
    return customers

@router.get("/{tracking_number}", response_model=CustomerResponse)
async def get_customer_by_tracking(
    tracking_number: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Obtener cliente por número de tracking"""
    customer = db.query(Customer).filter(Customer.tracking_number == tracking_number).first()
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado"
        )
    
    return customer
# Commit 16 - 2024-01-15
# Change: 1757423579
# Commit 18 - 2024-01-17
# Change: 1757423579
# Commit 22 - 2024-01-21
# Change: 1757423580
# Commit 26 - 2024-01-24
# Change: 1757423580
# Commit 53 - 2024-02-18
# Change: 1757423582
# Commit 66 - 2024-03-01
# Change: 1757423582
# Commit 67 - 2024-03-02
# Change: 1757423582
# Commit 78 - 2024-03-12
# Change: 1757423583
# Commit 92 - 2024-03-25
# Change: 1757423583
# Commit 95 - 2024-03-28
# Change: 1757423584
# Commit 107 - 2024-04-08
# Change: 1757423584
# Commit 120 - 2024-04-20
# Change: 1757423585
# Commit 123 - 2024-04-22
# Change: 1757423585
# Commit 124 - 2024-04-23
# Change: 1757423585
# Commit 131 - 2024-04-30
# Change: 1757423585
# Commit 132 - 2024-05-01
# Change: 1757423585
# Commit 143 - 2024-05-11
# Change: 1757423586
# Commit 146 - 2024-05-13
# Change: 1757423586
# Commit 151 - 2024-05-18
# Change: 1757423586
# Commit 153 - 2024-05-20
# Change: 1757423587
# Commit 179 - 2024-06-13
# Change: 1757423588
# Commit 226 - 2024-07-26
# Change: 1757423590
# Commit 240 - 2024-08-08
# Change: 1757423591
# Commit 271 - 2024-09-05
# Change: 1757423592
# Commit 284 - 2024-09-17
# Change: 1757423593
# Commit 295 - 2024-09-27
# Change: 1757423593
# Commit 311 - 2024-10-12
# Change: 1757423594
# Commit 335 - 2024-11-03
# Change: 1757423595
# Commit 345 - 2024-11-12
# Change: 1757423596
# Commit 387 - 2024-12-20
# Change: 1757423598
