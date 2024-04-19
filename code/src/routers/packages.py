# ========================================
# PAQUETES EL CLUB v3.1 - Router de Paquetes
# ========================================

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
import logging
from datetime import datetime

from ..database.database import get_db
from ..models.package import Package, PackageStatus
from ..models.user_activity_log import UserActivityLog, ActivityType
from ..models.user import User
from ..utils.datetime_utils import get_colombia_now
from ..dependencies import get_current_active_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/packages", tags=["packages"])

@router.get("/", response_model=List[dict])
async def list_packages(
    skip: int = 0,
    limit: int = 100,
    status_filter: Optional[PackageStatus] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Listar todos los paquetes con filtros opcionales"""
    
    query = db.query(Package)
    
    if status_filter:
        query = query.filter(Package.status == status_filter)
    
    packages = query.offset(skip).limit(limit).all()
    
    return [
        {
            "id": str(p.id),
            "tracking_number": p.tracking_number,
            "customer_name": p.customer_name,
            "customer_phone": p.customer_phone,
            "status": p.status.value,
            "package_type": p.package_type.value,
            "package_condition": p.package_condition.value,
            "total_cost": float(p.total_cost) if p.total_cost else 0,
            "announced_at": p.announced_at.isoformat() if p.announced_at else None,
            "received_at": p.received_at.isoformat() if p.received_at else None,
            "delivered_at": p.delivered_at.isoformat() if p.delivered_at else None
        }
        for p in packages
    ]

@router.get("/{package_id}", response_model=dict)
async def get_package(
    package_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtener paquete específico por ID"""
    
    package = db.query(Package).filter(Package.id == package_id).first()
    
    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paquete no encontrado"
        )
    
    return {
        "id": str(package.id),
        "tracking_number": package.tracking_number,
        "customer_name": package.customer_name,
        "customer_phone": package.customer_phone,
        "status": package.status.value,
        "package_type": package.package_type.value,
        "package_condition": package.package_condition.value,
        "storage_cost": float(package.storage_cost) if package.storage_cost else 0,
        "delivery_cost": float(package.delivery_cost) if package.delivery_cost else 0,
        "total_cost": float(package.total_cost) if package.total_cost else 0,
        "observations": package.observations,
        "announced_at": package.announced_at.isoformat() if package.announced_at else None,
        "received_at": package.received_at.isoformat() if package.received_at else None,
        "delivered_at": package.delivered_at.isoformat() if package.delivered_at else None
    }

@router.post("/{package_id}/receive")
async def receive_package(
    package_id: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Marcar paquete como recibido"""
    
    package = db.query(Package).filter(Package.id == package_id).first()
    
    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paquete no encontrado"
        )
    
    if package.status != PackageStatus.ANUNCIADO:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede recibir un paquete en estado {package.status.value}"
        )
    
    # Cambiar estado a RECIBIDO
    package.status = PackageStatus.RECIBIDO
    package.received_at = get_colombia_now()
    
    # Calcular costos automáticamente con el nuevo sistema
    from ..services.rate_service import RateService
    rate_service = RateService(db)
    
    # Calcular costo base según tipo de paquete
    base_costs = rate_service.calculate_package_costs(package.package_type)
    package.storage_cost = base_costs["storage_cost"]
    package.delivery_cost = base_costs["delivery_cost"]
    package.total_cost = base_costs["total_cost"]
    
    # Registrar actividad
    activity_log = UserActivityLog(
        user_id=current_user.id,
        activity_type=ActivityType.STATUS_CHANGE,
        description=f"Paquete {package.tracking_number} marcado como RECIBIDO - Costo: ${package.total_cost:,.0f}",
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
        activity_metadata={
            "package_id": str(package.id),
            "old_status": "anunciado",
            "new_status": "recibido",
            "action": "receive",
            "cost_calculated": float(package.total_cost),
            "package_type": package.package_type.value
        }
    )
    
    db.add(activity_log)
    db.commit()
    db.refresh(package)
    
    logger.info(f"Paquete {package.tracking_number} marcado como RECIBIDO por usuario {current_user.email} - Costo: ${package.total_cost:,.0f}")
    
    return {
        "success": True,
        "message": f"Paquete {package.tracking_number} marcado como RECIBIDO",
        "package_id": str(package.id),
        "new_status": package.status.value,
        "received_at": package.received_at.isoformat(),
        "cost_calculated": float(package.total_cost)
    }

@router.post("/{package_id}/deliver")
async def deliver_package(
    package_id: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Marcar paquete como entregado"""
    
    package = db.query(Package).filter(Package.id == package_id).first()
    
    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paquete no encontrado"
        )
    
    if package.status != PackageStatus.RECIBIDO:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede entregar un paquete en estado {package.status.value}"
        )
    
    # Calcular costos por tiempo excedido antes de entregar
    from ..services.rate_service import RateService
    rate_service = RateService(db)
    
    # Calcular costo total incluyendo tiempo excedido
    total_costs = rate_service.calculate_total_package_cost(
        package.package_type,
        package.received_at,
        get_colombia_now()
    )
    
    # Actualizar costos si hay tiempo excedido
    if total_costs["overtime_cost"] > 0:
        package.total_cost = total_costs["total_cost"]
        overtime_message = f" (Incluye ${total_costs['overtime_cost']:,.0f} por tiempo excedido)"
    else:
        overtime_message = ""
    
    # Cambiar estado a ENTREGADO
    package.status = PackageStatus.ENTREGADO
    package.delivered_at = get_colombia_now()
    
    # Registrar actividad
    activity_log = UserActivityLog(
        user_id=current_user.id,
        activity_type=ActivityType.STATUS_CHANGE,
        description=f"Paquete {package.tracking_number} marcado como ENTREGADO - Costo final: ${package.total_cost:,.0f}{overtime_message}",
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
        activity_metadata={
            "package_id": str(package.id),
            "old_status": "recibido",
            "new_status": "entregado",
            "action": "deliver",
            "final_cost": float(package.total_cost),
            "overtime_cost": total_costs["overtime_cost"],
            "overtime_hours": total_costs["overtime_hours"]
        }
    )
    
    db.add(activity_log)
    db.commit()
    db.refresh(package)
    
    logger.info(f"Paquete {package.tracking_number} marcado como ENTREGADO por usuario {current_user.email} - Costo final: ${package.total_cost:,.0f}")
    
    return {
        "success": True,
        "message": f"Paquete {package.tracking_number} marcado como ENTREGADO",
        "package_id": str(package.id),
        "new_status": package.status.value,
        "delivered_at": package.delivered_at.isoformat(),
        "final_cost": float(package.total_cost),
        "overtime_cost": total_costs["overtime_cost"],
        "overtime_hours": total_costs["overtime_hours"]
    }

@router.post("/{package_id}/cancel")
async def cancel_package(
    package_id: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Cancelar paquete (solo administradores)"""
    
    # Verificar que el usuario sea administrador
    if current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden cancelar paquetes"
        )
    
    package = db.query(Package).filter(Package.id == package_id).first()
    
    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paquete no encontrado"
        )
    
    if package.status == PackageStatus.CANCELADO:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El paquete ya está cancelado"
        )
    
    old_status = package.status.value
    
    # Cambiar estado a CANCELADO
    package.status = PackageStatus.CANCELADO
    
    # Registrar actividad
    activity_log = UserActivityLog(
        user_id=current_user.id,
        activity_type=ActivityType.STATUS_CHANGE,
        description=f"Paquete {package.tracking_number} CANCELADO desde estado {old_status} por administrador",
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
        activity_metadata={
            "package_id": str(package.id),
            "old_status": old_status,
            "new_status": "cancelado",
            "action": "cancel",
            "cancelled_by_admin": True
        }
    )
    
    db.add(activity_log)
    db.commit()
    db.refresh(package)
    
    logger.info(f"Paquete {package.tracking_number} CANCELADO desde estado {old_status} por administrador {current_user.email}")
    
    return {
        "success": True,
        "message": f"Paquete {package.tracking_number} cancelado exitosamente por administrador",
        "package_id": str(package.id),
        "new_status": package.status.value,
        "old_status": old_status
    }

@router.put("/{package_id}")
async def update_package(
    package_id: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Actualizar información del paquete"""
    
    package = db.query(Package).filter(Package.id == package_id).first()
    
    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paquete no encontrado"
        )
    
    # Obtener datos del request
    body = await request.json()
    
    # Actualizar campos permitidos
    if "package_type" in body:
        package.package_type = body["package_type"]
    
    if "package_condition" in body:
        package.package_condition = body["package_condition"]
    
    if "observations" in body:
        package.observations = body["observations"]
    
    # Registrar actividad
    activity_log = UserActivityLog(
        user_id=current_user.id,
        activity_type=ActivityType.STATUS_CHANGE,
        description=f"Información del paquete {package.tracking_number} actualizada",
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
        activity_metadata={
            "package_id": str(package.id),
            "action": "update_info",
            "updated_fields": list(body.keys())
        }
    )
    
    db.add(activity_log)
    db.commit()
    db.refresh(package)
    
    logger.info(f"Paquete {package.tracking_number} actualizado por usuario {current_user.email}")
    
    return {
        "success": True,
        "message": f"Paquete {package.tracking_number} actualizado exitosamente",
        "package_id": str(package.id)
    }

@router.get("/{package_id}/cost-calculation")
async def calculate_package_cost(
    package_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Calcular costo actual del paquete incluyendo tiempo excedido"""
    
    package = db.query(Package).filter(Package.id == package_id).first()
    
    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paquete no encontrado"
        )
    
    from ..services.rate_service import RateService
    rate_service = RateService(db)
    
    # Calcular costo total
    if package.status == PackageStatus.RECIBIDO and package.received_at:
        # Si está recibido, calcular con tiempo excedido
        total_costs = rate_service.calculate_total_package_cost(
            package.package_type,
            package.received_at,
            get_colombia_now()
        )
    else:
        # Si no está recibido, solo costo base
        base_costs = rate_service.calculate_package_costs(package.package_type)
        total_costs = {
            "base_cost": base_costs["total_cost"],
            "overtime_cost": 0.0,
            "total_cost": base_costs["total_cost"],
            "overtime_hours": 0,
            "overtime_periods": 0,
            "currency": "COP"
        }
    
    return {
        "package_id": str(package.id),
        "tracking_number": package.tracking_number,
        "status": package.status.value,
        "package_type": package.package_type.value,
        "current_cost": float(package.total_cost) if package.total_cost else 0,
        "calculated_cost": total_costs,
        "received_at": package.received_at.isoformat() if package.received_at else None,
        "grace_period_hours": 24,
        "overtime_rate_per_24h": 1000.0
    }

@router.get("/{package_id}/history")
async def get_package_history(
    package_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtener historial completo de un paquete"""
    
    package = db.query(Package).filter(Package.id == package_id).first()
    
    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paquete no encontrado"
        )
    
    # Obtener logs de actividad relacionados con este paquete
    activity_logs = db.query(UserActivityLog).filter(
        and_(
            UserActivityLog.activity_type == ActivityType.STATUS_CHANGE,
            UserActivityLog.activity_metadata.contains({"package_id": package_id})
        )
    ).order_by(UserActivityLog.created_at.asc()).all()
    
    # Construir historial
    history = []
    
    # Estado inicial: ANUNCIADO
    history.append({
        "status": "anunciado",
        "description": f"Paquete anunciado para {package.customer_name}",
        "timestamp": package.announced_at.isoformat() if package.announced_at else package.created_at.isoformat(),
        "details": {
            "customer_name": package.customer_name,
            "customer_phone": package.customer_phone,
            "tracking_number": package.tracking_number
        }
    })
    
    # Agregar cambios de estado desde los logs
    for log in activity_logs:
        metadata = log.activity_metadata
        if metadata.get("action") == "receive":
            history.append({
                "status": "recibido",
                "description": f"Paquete recibido en almacén",
                "timestamp": log.created_at.isoformat(),
                "details": {
                    "received_by": current_user.email,
                    "received_at": log.created_at.isoformat()
                }
            })
        elif metadata.get("action") == "deliver":
            history.append({
                "status": "entregado",
                "description": f"Paquete entregado al cliente",
                "timestamp": log.created_at.isoformat(),
                "details": {
                    "delivered_by": current_user.email,
                    "delivered_at": log.created_at.isoformat()
                }
            })
        elif metadata.get("action") == "cancel":
            history.append({
                "status": "cancelado",
                "description": f"Paquete cancelado desde estado {metadata.get('old_status', 'desconocido')}",
                "timestamp": log.created_at.isoformat(),
                "details": {
                    "cancelled_by": current_user.email,
                    "cancelled_at": log.created_at.isoformat(),
                    "previous_status": metadata.get('old_status', 'desconocido')
                }
            })
        elif metadata.get("action") == "update_info":
            history.append({
                "status": "actualizado",
                "description": f"Información del paquete actualizada",
                "timestamp": log.created_at.isoformat(),
                "details": {
                    "updated_by": current_user.email,
                    "updated_at": log.created_at.isoformat(),
                    "updated_fields": metadata.get('updated_fields', [])
                }
            })
    
    return {
        "package": {
            "id": str(package.id),
            "tracking_number": package.tracking_number,
            "customer_name": package.customer_name,
            "customer_phone": package.customer_phone,
            "status": package.status.value,
            "total_cost": float(package.total_cost) if package.total_cost else 0
        },
        "history": history
    }
# Commit 13 - 2024-01-12
# Change: 1757423579
# Commit 30 - 2024-01-28
# Change: 1757423580
# Commit 46 - 2024-02-12
# Change: 1757423581
# Commit 47 - 2024-02-13
# Change: 1757423581
# Commit 56 - 2024-02-21
# Change: 1757423582
# Commit 57 - 2024-02-22
# Change: 1757423582
# Commit 63 - 2024-02-27
# Change: 1757423582
# Commit 65 - 2024-02-29
# Change: 1757423582
# Commit 101 - 2024-04-02
# Change: 1757423584
# Commit 104 - 2024-04-05
# Change: 1757423584
# Commit 105 - 2024-04-06
# Change: 1757423584
# Commit 119 - 2024-04-19
# Change: 1757423585
