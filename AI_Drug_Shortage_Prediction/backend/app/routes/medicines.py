from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Medicine, User
from app.schemas import MedicineCreate, MedicineUpdate, MedicineResponse
from app.security import get_current_user, get_current_admin

router = APIRouter(prefix="/api/medicines", tags=["Medicines"])


@router.get("", response_model=List[MedicineResponse])
async def get_medicines(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all medicines with pagination"""
    medicines = db.query(Medicine).offset(skip).limit(limit).all()
    return medicines


@router.get("/low-stock", response_model=List[MedicineResponse])
async def get_low_stock_medicines(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get medicines with low stock"""
    medicines = db.query(Medicine).filter(
        Medicine.current_stock <= Medicine.reorder_level
    ).all()
    return medicines


@router.get("/out-of-stock", response_model=List[MedicineResponse])
async def get_out_of_stock_medicines(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get out of stock medicines"""
    medicines = db.query(Medicine).filter(
        Medicine.current_stock == 0
    ).all()
    return medicines


@router.get("/{medicine_id}", response_model=MedicineResponse)
async def get_medicine(
    medicine_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific medicine by ID"""
    medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    
    if not medicine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medicine not found"
        )
    
    return medicine


@router.post("", response_model=MedicineResponse, status_code=status.HTTP_201_CREATED)
async def create_medicine(
    medicine: MedicineCreate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Create a new medicine (Admin only)"""
    
    # Check if medicine already exists
    existing = db.query(Medicine).filter(
        Medicine.medicine_name == medicine.medicine_name
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Medicine already exists"
        )
    
    db_medicine = Medicine(**medicine.dict())
    db.add(db_medicine)
    db.commit()
    db.refresh(db_medicine)
    
    return db_medicine


@router.put("/{medicine_id}", response_model=MedicineResponse)
async def update_medicine(
    medicine_id: int,
    medicine: MedicineUpdate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Update a medicine (Admin only)"""
    
    db_medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    
    if not db_medicine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medicine not found"
        )
    
    # Update only provided fields
    update_data = medicine.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_medicine, field, value)
    
    db.commit()
    db.refresh(db_medicine)
    
    return db_medicine


@router.delete("/{medicine_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_medicine(
    medicine_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Delete a medicine (Admin only)"""
    
    db_medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    
    if not db_medicine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medicine not found"
        )
    
    db.delete(db_medicine)
    db.commit()
    
    return None
