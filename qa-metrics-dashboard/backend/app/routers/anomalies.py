from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.anomaly import AnomalyService
from ..schemas import MetricSeriesQuery, AnomalyOut
from ..auth import require_role

router = APIRouter(prefix="/anomalies", tags=["anomalies"])

@router.post("/detect", response_model=list[AnomalyOut], dependencies=[Depends(require_role("admin", "viewer"))])
def detect(q: MetricSeriesQuery, db: Session = Depends(get_db)):
    svc = AnomalyService(db)
    results = svc.detect_for(q.pipeline, q.name)
    return [AnomalyOut(ts=r["ts"], value=r["value"], score=r["score"]) for r in results]
