from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum


class User(Base):
    """User model for authentication"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password_hash = Column(String(255))
    role = Column(String(20), default="pharmacist")  # admin, pharmacist, manager
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sales = relationship("Sale", back_populates="pharmacist")
    predictions = relationship("Prediction", back_populates="user")


class Medicine(Base):
    """Medicine model"""
    __tablename__ = "medicines"
    
    id = Column(Integer, primary_key=True, index=True)
    medicine_name = Column(String(100), unique=True, index=True)
    category = Column(String(50))
    manufacturer = Column(String(100))
    batch_number = Column(String(50))
    barcode = Column(String(100), unique=True, index=True)
    expiry_date = Column(String(10))
    price = Column(Float)
    age_group = Column(String(50))
    uses = Column(Text)
    dosage = Column(String(100))
    prescription_required = Column(Boolean, default=False)
    side_effects = Column(Text)
    storage = Column(String(200))
    current_stock = Column(Integer, default=0)
    reorder_level = Column(Integer, default=50)
    shelf_location = Column(String(50))
    image_path = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sales = relationship("Sale", back_populates="medicine")
    predictions = relationship("Prediction", back_populates="medicine")


class Sale(Base):
    """Sale transaction model"""
    __tablename__ = "sales"
    
    id = Column(Integer, primary_key=True, index=True)
    medicine_id = Column(Integer, ForeignKey("medicines.id"))
    medicine_name = Column(String(100))
    batch_number = Column(String(50))
    quantity = Column(Integer)
    unit_price = Column(Float)
    total_amount = Column(Float)
    sale_date = Column(DateTime, default=datetime.utcnow)
    pharmacist_id = Column(Integer, ForeignKey("users.id"))
    customer_type = Column(String(20))  # retail, wholesale, hospital
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    medicine = relationship("Medicine", back_populates="sales")
    pharmacist = relationship("User", back_populates="sales")


class PredictionStatus(str, enum.Enum):
    SHORTAGE = "shortage"
    AVAILABLE = "available"
    LOW_STOCK = "low_stock"
    OVERSTOCKED = "overstocked"


class Prediction(Base):
    """AI prediction model"""
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    medicine_id = Column(Integer, ForeignKey("medicines.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    prediction_status = Column(SQLEnum(PredictionStatus), default=PredictionStatus.AVAILABLE)
    confidence = Column(Float)  # 0-100%
    predicted_shortage_days = Column(Integer, nullable=True)
    demand_quantity = Column(Integer)
    available_stock = Column(Integer)
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    rainfall = Column(Float, nullable=True)
    age_group = Column(String(20), nullable=True)
    severity = Column(String(20), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    medicine = relationship("Medicine", back_populates="predictions")
    user = relationship("User", back_populates="predictions")


class Alert(Base):
    """Alert model for notifications"""
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    medicine_id = Column(Integer, ForeignKey("medicines.id"))
    alert_type = Column(String(50))  # out_of_stock, low_stock, expiry, temperature, etc
    message = Column(Text)
    severity = Column(String(20))  # critical, warning, info
    is_resolved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)


class AuditLog(Base):
    """Audit log for tracking changes"""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String(100))
    entity_type = Column(String(50))
    entity_id = Column(Integer)
    old_values = Column(Text, nullable=True)
    new_values = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
