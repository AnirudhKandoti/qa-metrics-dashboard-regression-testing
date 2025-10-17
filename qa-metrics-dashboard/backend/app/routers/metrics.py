from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..database import get_db
from ..models import Pipeline, Metric
from ..schemas import MetricPoint, MetricSeriesQuery, MetricSeriesOut, MetricSeriesPoint
from ..auth import require_role

router = APIRouter(prefix="/metrics", tags=["metrics"])

@router.post("/ingest", dependencies=[Depends(require_role("admin"))])
def ingest(points: list[MetricPoint], db: Session = Depends(get_db)):
    pipelines = {p.name: p for p in db.query(Pipeline).all()}
    for pt in points:
        p = pipelines.get(pt.pipeline)
        if p is None:
            p = Pipeline(name=pt.pipeline)
            db.add(p); db.flush()
            pipelines[p.name] = p
        db.add(Metric(pipeline_id=p.id, name=pt.name, ts=pt.ts, value=pt.value))
    db.commit()
    return {"ingested": len(points)}

@router.post("/series", response_model=MetricSeriesOut)
def series(q: MetricSeriesQuery, db: Session = Depends(get_db)):
    p = db.query(Pipeline).filter(Pipeline.name == q.pipeline).first()
    if not p:
        raise HTTPException(404, "Pipeline not found")
    stmt = (
        select(Metric)
        .where(Metric.pipeline_id == p.id, Metric.name == q.name)
        .order_by(Metric.ts.asc())
    )
    rows = db.execute(stmt).scalars().all()
    points = [MetricSeriesPoint(ts=r.ts, value=r.value) for r in rows if (q.since is None or r.ts >= q.since) and (q.until is None or r.ts <= q.until)]
    return MetricSeriesOut(pipeline=q.pipeline, name=q.name, points=points)
