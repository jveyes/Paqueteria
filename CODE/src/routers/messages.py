# ========================================
# PAQUETES EL CLUB v3.0 - Router de Mensajes
# ========================================

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from typing import List, Optional
import uuid

from ..database.database import get_db
from ..models.message import Message, MessageType, MessageStatus, MessagePriority
from ..models.user import User
from ..schemas.message import (
    CustomerInquiryCreate, 
    MessageResponse, 
    MessageList, 
    MessageDetail, 
    MessageStats
)
from ..dependencies import get_current_active_user
from datetime import datetime

router = APIRouter()

@router.post("/customer-inquiry", status_code=status.HTTP_201_CREATED)
async def create_customer_inquiry(
    inquiry: CustomerInquiryCreate,
    db: Session = Depends(get_db)
):
    """Crear consulta de cliente (pública)"""
    try:
        # Crear nuevo mensaje
        message = Message(
            customer_name=inquiry.customer_name,
            customer_phone=inquiry.customer_phone,
            customer_email=inquiry.customer_email,
            package_guide_number=inquiry.package_guide_number,
            package_tracking_code=inquiry.package_tracking_code,
            subject=inquiry.subject,
            content=inquiry.content,
            message_type=MessageType.CUSTOMER_INQUIRY
            # status se establece automáticamente como UNREAD por defecto
        )
        
        db.add(message)
        db.commit()
        db.refresh(message)
        
        return {
            "message": "Consulta enviada exitosamente",
            "id": str(message.id),
            "status": "unread"
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear consulta: {str(e)}"
        )

@router.get("/check-inquiry-exists")
async def check_inquiry_exists(
    customer_email: str = Query(..., description="Email del cliente"),
    package_tracking_code: str = Query(..., description="Código de tracking del paquete"),
    db: Session = Depends(get_db)
):
    """Verificar si ya existe una consulta previa para este email y paquete"""
    try:
        # Buscar consultas existentes con el mismo email y código de tracking
        existing_inquiry = db.query(Message).filter(
            and_(
                Message.customer_email == customer_email,
                Message.package_tracking_code == package_tracking_code,
                Message.message_type == MessageType.CUSTOMER_INQUIRY
            )
        ).first()
        
        # Verificar si existe y si está en estado pendiente (UNREAD o PENDING)
        has_pending_inquiry = existing_inquiry and existing_inquiry.status in [MessageStatus.UNREAD, MessageStatus.PENDING]
        
        return {
            "exists": existing_inquiry is not None,
            "has_pending": has_pending_inquiry,
            "inquiry_id": str(existing_inquiry.id) if existing_inquiry else None,
            "status": existing_inquiry.status.value if existing_inquiry else None,
            "created_at": existing_inquiry.created_at.isoformat() if existing_inquiry else None
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al verificar consulta existente: {str(e)}"
        )

@router.get("/check-tracking-inquiries")
async def check_tracking_inquiries(
    package_tracking_code: str = Query(..., description="Código de tracking del paquete"),
    db: Session = Depends(get_db)
):
    """Verificar si ya existen consultas para este código de tracking"""
    try:
        # Buscar todas las consultas existentes para este código de tracking
        existing_inquiries = db.query(Message).filter(
            and_(
                Message.package_tracking_code == package_tracking_code,
                Message.message_type == MessageType.CUSTOMER_INQUIRY
            )
        ).all()
        
        # Si hay consultas, devolver la más reciente y información de estados
        if existing_inquiries:
            latest_inquiry = max(existing_inquiries, key=lambda x: x.created_at)
            
            # Verificar si hay algún mensaje con estado PENDING o UNREAD
            has_pending = any(inquiry.status in [MessageStatus.PENDING, MessageStatus.UNREAD] for inquiry in existing_inquiries)
            has_unread = any(inquiry.status == MessageStatus.UNREAD for inquiry in existing_inquiries)
            
            return {
                "exists": True,
                "count": len(existing_inquiries),
                "has_pending": has_pending,
                "has_unread": has_unread,
                "latest_inquiry": {
                    "id": str(latest_inquiry.id),
                    "customer_email": latest_inquiry.customer_email,
                    "status": latest_inquiry.status,
                    "created_at": latest_inquiry.created_at.isoformat()
                },
                "inquiries": [
                    {
                        "id": str(inquiry.id),
                        "status": inquiry.status,
                        "created_at": inquiry.created_at.isoformat()
                    } for inquiry in existing_inquiries
                ]
            }
        
        return {
            "exists": False,
            "count": 0,
            "latest_inquiry": None
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al verificar consultas del tracking: {str(e)}"
        )

@router.get("/test")
async def test_messages():
    """Endpoint de prueba simple"""
    return {"message": "Endpoint funcionando", "timestamp": datetime.now().isoformat()}

@router.get("/tracking/{tracking_code}")
async def get_messages_by_tracking_code(
    tracking_code: str,
    db: Session = Depends(get_db)
):
    """Obtener mensajes por código de tracking (público)"""
    try:
        # Buscar mensajes por código de tracking con relaciones
        messages = db.query(Message).filter(
            Message.package_tracking_code == tracking_code.upper()
        ).order_by(desc(Message.created_at)).all()
        
        # Convertir a formato de respuesta
        result = []
        for message in messages:
            # Obtener username del administrador que respondió
            admin_username = None
            if message.responded_by:
                admin_username = message.responded_by.username
            
            result.append({
                "id": str(message.id),
                "customer_name": message.customer_name,
                "customer_phone": message.customer_phone,
                "customer_email": message.customer_email,
                "package_guide_number": message.package_guide_number,
                "package_tracking_code": message.package_tracking_code,
                "subject": message.subject,
                "content": message.content,
                "message_type": message.message_type.value if hasattr(message.message_type, 'value') else str(message.message_type),
                "status": message.status.value if hasattr(message.status, 'value') else str(message.status),
                "created_at": message.created_at.isoformat(),
                "updated_at": message.updated_at.isoformat() if message.updated_at else None,
                "admin_response": message.admin_response,
                "responded_at": message.responded_at.isoformat() if message.responded_at else None,
                "admin_username": admin_username
            })
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener mensajes: {str(e)}"
        )

@router.get("/")
async def list_messages(
    page: int = Query(1, ge=1, description="Número de página"),
    limit: int = Query(20, ge=1, le=100, description="Elementos por página"),
    status: Optional[str] = Query(None, description="Filtrar por estado"),
    message_type: Optional[MessageType] = Query(None, description="Filtrar por tipo de mensaje"),
    priority: Optional[MessagePriority] = Query(None, description="Filtrar por prioridad"),
    search: Optional[str] = Query(None, description="Búsqueda en nombre, teléfono o contenido"),
    unread_only: bool = Query(False, description="Solo mensajes no leídos"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Listar mensajes con paginación y filtros (solo usuarios autenticados)"""
    try:
        # Construir query base
        query = db.query(Message)
        
        # Aplicar filtros
        if status:
            if status == "unread":
                # No Leídos: mensajes que no se han visualizado
                query = query.filter(Message.is_read == False)
            elif status == "pending":
                # Pendientes: mensajes que se visualizaron pero no tienen respuesta
                query = query.filter(
                    Message.is_read == True,
                    Message.admin_response.is_(None)
                )
            elif status == "closed":
                # Cerrados: mensajes que ya tienen respuesta (Resueltos)
                query = query.filter(Message.admin_response.isnot(None))
            else:
                # Filtro por estado tradicional (para compatibilidad)
                query = query.filter(Message.status == status)
        
        if message_type:
            query = query.filter(Message.message_type == message_type)
        
        if priority:
            query = query.filter(Message.priority == priority)
        
        # Remover el filtro unread_only para evitar conflictos
        # if unread_only and status != "unread":
        #     query = query.filter(Message.is_read == False)
        
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Message.customer_name.ilike(search_term),
                    Message.customer_phone.ilike(search_term),
                    Message.content.ilike(search_term),
                    Message.subject.ilike(search_term)
                )
            )
        
        # Aplicar paginación y ordenamiento (por prioridad y fecha)
        total = query.count()
        messages = query.order_by(
            Message.priority.desc(),  # Urgent primero, luego High, Normal, Low
            desc(Message.created_at)
        ).offset((page - 1) * limit).limit(limit).all()
        
        # Convertir a formato de respuesta
        result = []
        for message in messages:
            result.append({
                "id": str(message.id),
                "subject": message.subject,
                "content": message.content,
                "customer_name": message.customer_name,
                "customer_phone": message.customer_phone,
                "customer_email": message.customer_email,
                "is_read": message.is_read,
                "admin_response": message.admin_response,
                "status": message.status.value if hasattr(message.status, 'value') else str(message.status),  # Usar directamente el status de la BD
                "message_type": message.message_type.value if hasattr(message.message_type, 'value') else str(message.message_type),
                "priority": message.priority.value if hasattr(message.priority, 'value') else str(message.priority),
                "created_at": message.created_at.isoformat(),
                "package_guide_number": message.package_guide_number,
                "package_tracking_code": message.package_tracking_code
            })
        
        # Calcular información de paginación
        total_pages = (total + limit - 1) // limit
        has_next = page < total_pages
        has_prev = page > 1
        
        return {
            "messages": result,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "total_pages": total_pages,
                "has_next": has_next,
                "has_prev": has_prev
            }
        }
        
    except Exception as e:
        # Log del error para debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error en list_messages: {str(e)}", exc_info=True)
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al obtener mensajes"
        )

@router.get("/stats", response_model=MessageStats)
async def get_message_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtener estadísticas de mensajes"""
    try:
        total_messages = db.query(Message).count()
        
        # No Leídos: mensajes que no se han visualizado
        unread_messages = db.query(Message).filter(Message.is_read == False).count()
        
        # Pendientes: mensajes que se visualizaron pero no tienen respuesta
        pending_messages = db.query(Message).filter(
            Message.is_read == True,
            Message.admin_response.is_(None)
        ).count()
        
        # Cerrados: mensajes que ya tienen respuesta
        closed_messages = db.query(Message).filter(Message.admin_response.isnot(None)).count()
        
        return MessageStats(
            total_messages=total_messages,
            pending_messages=pending_messages,
            closed_messages=closed_messages,
            unread_messages=unread_messages
        )
    except Exception as e:
        # Log del error para debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error en get_message_stats: {str(e)}", exc_info=True)
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al obtener estadísticas"
        )

@router.get("/{message_id}", response_model=MessageDetail)
async def get_message_detail(
    message_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtener detalle de un mensaje"""
    try:
        message = db.query(Message).filter(Message.id == uuid.UUID(message_id)).first()
        
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mensaje no encontrado"
            )
        
        # Marcar como leído solo cuando el admin explícitamente lo lee
        # Comentado para permitir el flujo correcto: UNREAD → PENDING → CLOSED
        # if not message.is_read:
        #     message.mark_as_read(current_user.id)
        #     db.commit()
        
        # Obtener nombres de usuarios relacionados
        read_by_name = None
        if message.read_by:
            read_by_name = message.read_by.full_name
        
        responded_by_name = None
        if message.responded_by:
            responded_by_name = message.responded_by.full_name
        
        return MessageDetail(
            id=str(message.id),
            customer_name=message.customer_name,
            customer_phone=message.customer_phone,
            customer_email=message.customer_email,
            subject=message.subject,
            content=message.content,
            message_type=message.message_type,
            status=message.status,  # Usar directamente el status de la BD
            priority=message.priority,
            is_read=message.is_read,
            read_at=message.read_at,
            read_by_name=read_by_name,
            created_at=message.created_at,
            package_guide_number=message.package_guide_number,
            package_tracking_code=message.package_tracking_code,
            admin_response=message.admin_response,
            responded_at=message.responded_at,
            responded_by_name=responded_by_name
        )
        
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de mensaje inválido"
        )
    except Exception as e:
        # Log del error para debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error en get_message_detail: {str(e)}", exc_info=True)
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al obtener detalle del mensaje"
        )

@router.post("/{message_id}/read", status_code=status.HTTP_200_OK)
async def mark_message_as_read(
    message_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Marcar un mensaje como leído"""
    try:
        message = db.query(Message).filter(Message.id == uuid.UUID(message_id)).first()
        
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mensaje no encontrado"
            )
        
        # Marcar como leído
        if not message.is_read:
            message.mark_as_read(current_user.id)
            db.commit()
        
        return {
            "message": "Mensaje marcado como leído",
            "status": message.status.value if hasattr(message.status, 'value') else str(message.status)
        }
        
    except Exception as e:
        db.rollback()
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error en mark_message_as_read: {str(e)}", exc_info=True)
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al marcar mensaje como leído"
        )

@router.post("/{message_id}/respond", status_code=status.HTTP_200_OK)
async def respond_to_message(
    message_id: str,
    response_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Responder a un mensaje"""
    try:
        message = db.query(Message).filter(Message.id == uuid.UUID(message_id)).first()
        
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mensaje no encontrado"
            )
        
        # Validar que se proporcionó una respuesta
        response_text = response_data.get('response')
        if not response_text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El campo 'response' es requerido"
            )
        
        # Validar longitud de la respuesta
        if len(response_text.strip()) < 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La respuesta debe tener al menos 5 caracteres"
            )
        
        if len(response_text) > 2000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La respuesta no puede exceder 2000 caracteres"
            )
        
        # Marcar como leído si no lo está
        if not message.is_read:
            message.mark_as_read(current_user.id)
        
        # Responder al mensaje
        message.respond(response_text.strip(), current_user.id)
        db.commit()
        
        return {
            "message": "Respuesta enviada exitosamente. El mensaje ha sido cerrado automáticamente.",
            "status": "closed"
        }
        
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de mensaje inválido"
        )

@router.put("/{message_id}/status", status_code=status.HTTP_200_OK)
async def update_message_status(
    message_id: str,
    request: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Actualizar estado de un mensaje"""
    try:
        message = db.query(Message).filter(Message.id == uuid.UUID(message_id)).first()
        
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mensaje no encontrado"
            )
        
        new_status = request.get('new_status')
        if not new_status:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="new_status es requerido"
            )
        
        # Validar que el estado sea válido
        try:
            status_enum = MessageStatus(new_status)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Estado inválido: {new_status}"
            )
        
        message.status = status_enum
        message.updated_at = datetime.now()
        db.commit()
        
        return {
            "message": "Estado actualizado exitosamente",
            "status": new_status
        }
        
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de mensaje inválido"
        )

@router.delete("/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(
    message_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Eliminar un mensaje (solo administradores)"""
    try:
        message = db.query(Message).filter(Message.id == uuid.UUID(message_id)).first()
        
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mensaje no encontrado"
            )
        
        db.delete(message)
        db.commit()
        
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de mensaje inválido"
        )