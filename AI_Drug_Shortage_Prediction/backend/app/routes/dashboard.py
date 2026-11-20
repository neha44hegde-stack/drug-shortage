from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import Medicine, Sale, User, Alert, Prediction, PredictionStatus
from app.schemas import DashboardStats
from app.security import get_current_user
from datetime import datetime

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get dashboard statistics"""
    
    # Count medicines
    total_medicines = db.query(func.count(Medicine.id)).scalar() or 0
    
    # Count low stock medicines
    low_stock = db.query(func.count(Medicine.id)).filter(
        Medicine.current_stock <= Medicine.reorder_level
    ).scalar() or 0
    
    # Count out of stock medicines
    out_of_stock = db.query(func.count(Medicine.id)).filter(
        Medicine.current_stock == 0
    ).scalar() or 0
    
    # Today's sales
    today = datetime.utcnow().date()
    today_sales = db.query(func.sum(Sale.total_amount)).filter(
        func.date(Sale.sale_date) == today
    ).scalar() or 0.0
    
    today_units = db.query(func.sum(Sale.quantity)).filter(
        func.date(Sale.sale_date) == today
    ).scalar() or 0
    
    # Critical alerts (unresolved)
    critical_alerts = db.query(func.count(Alert.id)).filter(
        (Alert.severity == "critical") & (Alert.is_resolved == False)
    ).scalar() or 0
    
    # Pending predictions (shortages)
    pending_predictions = db.query(func.count(Prediction.id)).filter(
        Prediction.prediction_status == PredictionStatus.SHORTAGE
    ).scalar() or 0
    
    return DashboardStats(
        total_medicines=total_medicines,
        low_stock_medicines=low_stock,
        out_of_stock_medicines=out_of_stock,
        total_sales_today=float(today_sales),
        total_units_sold_today=int(today_units),
        critical_alerts=critical_alerts,
        pending_predictions=pending_predictions
    )
