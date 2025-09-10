# ========================================
# PAQUETES EL CLUB v3.0 - Servicio de Tarifas
# ========================================

from sqlalchemy.orm import Session
from typing import Dict, Any
from decimal import Decimal
from datetime import datetime

from ..models.rate import Rate, RateType
from ..models.package import PackageType
from ..utils.exceptions import RateCalculationException
from ..utils.validators import validate_rate_calculation_params
from ..config import settings

class RateService:
    """Servicio para la lógica de negocio de tarifas"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def calculate_package_costs(
        self,
        package_type: PackageType,
        storage_days: int = 1,
        delivery_required: bool = True
    ) -> Dict[str, float]:
        """Calcular costos de un paquete con el nuevo sistema de tarifas"""
        # Tarifas fijas según el nuevo sistema
        base_rates = {
            PackageType.NORMAL: 1500.0,
            PackageType.EXTRA_DIMENSIONADO: 2000.0
        }
        
        # Costo base según tipo de paquete
        base_cost = base_rates.get(package_type, 1500.0)
        
        # Costo de entrega (incluido en la tarifa base)
        delivery_cost = 0 if delivery_required else 0
        
        # Calcular costos finales
        storage_cost = base_cost
        total_cost = storage_cost + delivery_cost
        
        return {
            "storage_cost": storage_cost,
            "delivery_cost": delivery_cost,
            "total_cost": total_cost,
            "currency": "COP"
        }
    
    def calculate_overtime_costs(
        self,
        package_type: PackageType,
        received_at: datetime,
        current_time: datetime = None
    ) -> Dict[str, float]:
        """Calcular costos adicionales por tiempo excedido"""
        from datetime import timedelta
        
        if current_time is None:
            from ..utils.datetime_utils import get_colombia_now
            current_time = get_colombia_now()
        
        # Calcular tiempo transcurrido desde que se recibió
        time_elapsed = current_time - received_at
        
        # 24 horas de gracia
        grace_period = timedelta(hours=24)
        
        # Si está dentro del período de gracia, no hay costo adicional
        if time_elapsed <= grace_period:
            return {
                "overtime_hours": 0,
                "overtime_cost": 0.0,
                "total_overtime_cost": 0.0
            }
        
        # Calcular horas excedidas (cada 24 horas = $1000 adicionales)
        overtime_hours = time_elapsed - grace_period
        overtime_periods = int(overtime_hours.total_seconds() / (24 * 3600)) + 1
        
        # Costo por período de 24 horas excedidas
        overtime_cost_per_period = 1000.0
        total_overtime_cost = overtime_periods * overtime_cost_per_period
        
        return {
            "overtime_hours": overtime_hours.total_seconds() / 3600,  # En horas
            "overtime_periods": overtime_periods,
            "overtime_cost_per_period": overtime_cost_per_period,
            "total_overtime_cost": total_overtime_cost
        }
    
    def calculate_total_package_cost(
        self,
        package_type: PackageType,
        received_at: datetime = None,
        current_time: datetime = None
    ) -> Dict[str, float]:
        """Calcular costo total del paquete incluyendo tiempo excedido"""
        # Costo base
        base_costs = self.calculate_package_costs(package_type)
        
        # Si no hay fecha de recepción, solo retornar costo base
        if not received_at:
            return base_costs
        
        # Calcular costos por tiempo excedido
        overtime_costs = self.calculate_overtime_costs(package_type, received_at, current_time)
        
        # Costo total
        total_cost = base_costs["total_cost"] + overtime_costs["total_overtime_cost"]
        
        return {
            "base_cost": base_costs["total_cost"],
            "overtime_cost": overtime_costs["total_overtime_cost"],
            "total_cost": total_cost,
            "overtime_hours": overtime_costs["overtime_hours"],
            "overtime_periods": overtime_costs["overtime_periods"],
            "currency": "COP"
        }
    
    def get_active_rates(self) -> Dict[str, Rate]:
        """Obtener todas las tarifas activas"""
        rates = self.db.query(Rate).filter(Rate.is_active == True).all()
        return {rate.rate_type.value: rate for rate in rates}
    
    def create_rate(self, rate_data: Dict[str, Any]) -> Rate:
        """Crear nueva tarifa"""
        # Desactivar tarifas anteriores del mismo tipo
        existing_rates = self.db.query(Rate).filter(
            Rate.rate_type == rate_data["rate_type"],
            Rate.is_active == True
        ).all()
        
        for rate in existing_rates:
            rate.is_active = False
        
        # Crear nueva tarifa
        new_rate = Rate(**rate_data)
        self.db.add(new_rate)
        self.db.commit()
        self.db.refresh(new_rate)
        
        return new_rate
    
    def update_rate(self, rate_id: str, rate_data: Dict[str, Any]) -> Rate:
        """Actualizar tarifa existente"""
        rate = self.db.query(Rate).filter(Rate.id == rate_id).first()
        
        if not rate:
            raise RateCalculationException(f"Tarifa con ID {rate_id} no encontrada")
        
        # Actualizar campos
        for field, value in rate_data.items():
            if hasattr(rate, field):
                setattr(rate, field, value)
        
        self.db.commit()
        self.db.refresh(rate)
        
        return rate
    
    def get_rate_history(self, rate_type: RateType = None) -> list:
        """Obtener historial de cambios de tarifas"""
        query = self.db.query(Rate)
        
        if rate_type:
            query = query.filter(Rate.rate_type == rate_type)
        
        return query.order_by(Rate.created_at.desc()).all()
    
    def _get_active_rate(self, rate_type: RateType) -> Rate:
        """Obtener tarifa activa por tipo"""
        return self.db.query(Rate).filter(
            Rate.rate_type == rate_type,
            Rate.is_active == True
        ).first()
    
    def get_rate_summary(self) -> Dict[str, Any]:
        """Obtener resumen de tarifas actuales"""
        active_rates = self.get_active_rates()
        
        summary = {
            "active_rates": len(active_rates),
            "rates_by_type": {}
        }
        
        for rate_type, rate in active_rates.items():
            summary["rates_by_type"][rate_type] = {
                "base_price": float(rate.base_price),
                "daily_storage_rate": float(rate.daily_storage_rate) if rate.daily_storage_rate else 0,
                "delivery_rate": float(rate.delivery_rate) if rate.delivery_rate else 0,
                "package_type_multiplier": float(rate.package_type_multiplier) if rate.package_type_multiplier else 1.0,
                "valid_from": rate.valid_from.isoformat() if rate.valid_from else None
            }
        
        return summary
