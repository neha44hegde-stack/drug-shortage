from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import List
from app.database import get_db
from app.models import Sale, Medicine, User
from app.schemas import SaleCreate, SaleResponse, SaleStats
from app.security import get_current_user

router = APIRouter(prefix="/api/sales", tags=["Sales"])


@router.get("", response_model=List[SaleResponse])
async def get_sales(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all sales with pagination"""
    sales = db.query(Sale).order_by(Sale.sale_date.desc()).offset(skip).limit(limit).all()
    return sales


@router.get("/statistics/today", response_model=SaleStats)
async def get_today_sales(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get sales statistics for today"""
    today = datetime.utcnow().date()
    
    result = db.query(
        func.count(Sale.id).label("total_transactions"),
        func.sum(Sale.quantity).label("total_quantity"),
        func.sum(Sale.total_amount).label("total_amount")
    ).filter(
        func.date(Sale.sale_date) == today
    ).first()
    
    total_transactions = result[0] or 0
    total_quantity = result[1] or 0
    total_amount = result[2] or 0.0
    average_transaction = total_amount / total_transactions if total_transactions > 0 else 0
    
    return SaleStats(
        total_transactions=total_transactions,
        total_quantity=total_quantity,
        total_amount=total_amount,
        average_transaction=average_transaction
    )


@router.get("/statistics/monthly", response_model=SaleStats)
async def get_monthly_sales(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get sales statistics for current month"""
    today = datetime.utcnow().date()
    month_start = today.replace(day=1)
    
    result = db.query(
        func.count(Sale.id).label("total_transactions"),
        func.sum(Sale.quantity).label("total_quantity"),
        func.sum(Sale.total_amount).label("total_amount")
    ).filter(
        func.date(Sale.sale_date) >= month_start
    ).first()
    
    total_transactions = result[0] or 0
    total_quantity = result[1] or 0
    total_amount = result[2] or 0.0
    average_transaction = total_amount / total_transactions if total_transactions > 0 else 0
    
    return SaleStats(
        total_transactions=total_transactions,
        total_quantity=total_quantity,
        total_amount=total_amount,
        average_transaction=average_transaction
    )


@router.get("/{sale_id}", response_model=SaleResponse)
async def get_sale(
    sale_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific sale"""
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    
    if not sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale not found"
        )
    
    return sale


@router.post("", response_model=SaleResponse, status_code=status.HTTP_201_CREATED)
async def create_sale(
    sale: SaleCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new sale"""
    
    # Get medicine
    medicine = db.query(Medicine).filter(Medicine.id == sale.medicine_id).first()
    
    if not medicine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medicine not found"
        )
    
    # Check stock
    if medicine.current_stock < sale.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient stock. Available: {medicine.current_stock}"
        )
    
    # Calculate total amount
    total_amount = medicine.price * sale.quantity
    
    # Create sale record
    db_sale = Sale(
        medicine_id=sale.medicine_id,
        medicine_name=medicine.medicine_name,
        batch_number=medicine.batch_number,
        quantity=sale.quantity,
        unit_price=medicine.price,
        total_amount=total_amount,
        pharmacist_id=current_user.id,
        customer_type=sale.customer_type
    )
    
    # Update stock
    medicine.current_stock -= sale.quantity
    
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    
    return db_sale
