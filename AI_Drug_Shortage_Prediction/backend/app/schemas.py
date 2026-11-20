from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    PHARMACIST = "pharmacist"
    MANAGER = "manager"


# ==================== USER SCHEMAS ====================

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    role: UserRole = UserRole.PHARMACIST


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== MEDICINE SCHEMAS ====================

class MedicineBase(BaseModel):
    medicine_name: str
    category: str
    manufacturer: str
    batch_number: str
    barcode: str
    expiry_date: str
    price: float = Field(..., gt=0)
    age_group: str
    uses: str
    dosage: str
    prescription_required: bool = False
    side_effects: str
    storage: str
    current_stock: int = Field(..., ge=0)
    reorder_level: int = Field(..., ge=0)
    shelf_location: str


class MedicineCreate(MedicineBase):
    pass


class MedicineUpdate(BaseModel):
    medicine_name: Optional[str] = None
    category: Optional[str] = None
    manufacturer: Optional[str] = None
    batch_number: Optional[str] = None
    expiry_date: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    current_stock: Optional[int] = Field(None, ge=0)
    reorder_level: Optional[int] = Field(None, ge=0)


class MedicineResponse(MedicineBase):
    id: int
    image_path: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== SALE SCHEMAS ====================

class SaleBase(BaseModel):
    medicine_id: int
    quantity: int = Field(..., gt=0)
    customer_type: str


class SaleCreate(SaleBase):
    pass


class SaleResponse(BaseModel):
    id: int
    medicine_id: int
    medicine_name: str
    batch_number: str
    quantity: int
    unit_price: float
    total_amount: float
    sale_date: datetime
    pharmacist_id: int
    customer_type: str
    notes: Optional[str]

    class Config:
        from_attributes = True


class SaleStats(BaseModel):
    total_transactions: int
    total_quantity: int
    total_amount: float
    average_transaction: float


# ==================== PREDICTION SCHEMAS ====================

class PredictionCreate(BaseModel):
    medicine_id: int
    demand_quantity: int = Field(..., gt=0)
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    rainfall: Optional[float] = None
    age_group: Optional[str] = None
    severity: Optional[str] = None


class PredictionResponse(BaseModel):
    id: int
    medicine_id: int
    medicine_name: str
    prediction_status: str
    confidence: float
    predicted_shortage_days: Optional[int]
    demand_quantity: int
    available_stock: int
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== ALERT SCHEMAS ====================

class AlertResponse(BaseModel):
    id: int
    medicine_id: int
    medicine_name: str
    alert_type: str
    message: str
    severity: str
    is_resolved: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== AUTHENTICATION SCHEMAS ====================

class TokenRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenPayload(BaseModel):
    sub: str
    exp: datetime
    iat: datetime


# ==================== DASHBOARD SCHEMAS ====================

class DashboardStats(BaseModel):
    total_medicines: int
    low_stock_medicines: int
    out_of_stock_medicines: int
    total_sales_today: float
    total_units_sold_today: int
    critical_alerts: int
    pending_predictions: int
