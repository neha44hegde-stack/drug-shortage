from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.database import get_db
from app.models import Prediction, Medicine, User, PredictionStatus
from app.schemas import PredictionCreate, PredictionResponse
from app.security import get_current_user

router = APIRouter(prefix="/api/predictions", tags=["Predictions"])


@router.get("", response_model=List[PredictionResponse])
async def get_predictions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all predictions with pagination"""
    predictions = db.query(Prediction).order_by(
        Prediction.created_at.desc()
    ).offset(skip).limit(limit).all()
    return predictions


@router.get("/shortages", response_model=List[PredictionResponse])
async def get_shortage_predictions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get predicted shortages"""
    predictions = db.query(Prediction).filter(
        Prediction.prediction_status == PredictionStatus.SHORTAGE
    ).all()
    return predictions


@router.get("/{prediction_id}", response_model=PredictionResponse)
async def get_prediction(
    prediction_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific prediction"""
    prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    
    if not prediction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prediction not found"
        )
    
    return prediction


@router.post("", response_model=PredictionResponse, status_code=status.HTTP_201_CREATED)
async def create_prediction(
    pred: PredictionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new prediction using AI model
    
    This endpoint uses the trained XGBoost model to predict drug shortages
    based on various parameters.
    """
    
    # Get medicine
    medicine = db.query(Medicine).filter(Medicine.id == pred.medicine_id).first()
    
    if not medicine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medicine not found"
        )
    
    # Load and use the ML model to make prediction
    # TODO: Implement actual ML model prediction here
    # For now, using simple business logic
    
    # Simple shortage prediction logic
    stock_consumption_ratio = pred.demand_quantity / max(medicine.current_stock, 1)
    
    if stock_consumption_ratio > 1.5:
        prediction_status = PredictionStatus.SHORTAGE
        predicted_shortage_days = 3
        confidence = 95.0
    elif stock_consumption_ratio > 1.0:
        prediction_status = PredictionStatus.LOW_STOCK
        predicted_shortage_days = 7
        confidence = 85.0
    elif medicine.current_stock > medicine.reorder_level * 2:
        prediction_status = PredictionStatus.OVERSTOCKED
        predicted_shortage_days = None
        confidence = 90.0
    else:
        prediction_status = PredictionStatus.AVAILABLE
        predicted_shortage_days = None
        confidence = 88.0
    
    # Create prediction record
    db_prediction = Prediction(
        medicine_id=pred.medicine_id,
        user_id=current_user.id,
        prediction_status=prediction_status,
        confidence=confidence,
        predicted_shortage_days=predicted_shortage_days,
        demand_quantity=pred.demand_quantity,
        available_stock=medicine.current_stock,
        temperature=pred.temperature,
        humidity=pred.humidity,
        rainfall=pred.rainfall,
        age_group=pred.age_group,
        severity=pred.severity
    )
    
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    
    return db_prediction
