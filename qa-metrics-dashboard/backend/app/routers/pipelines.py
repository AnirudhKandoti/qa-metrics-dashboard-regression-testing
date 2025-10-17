from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Pipeline
from ..schemas import PipelineCreate, PipelineOut
from ..auth import require_role

router = APIRouter(prefix="/pipelines", tags=["pipelines"])

@router.post("/", response_model=PipelineOut, dependencies=[Depends(require_role("admin"))])
def create_pipeline(body: PipelineCreate, db: Session = Depends(get_db)):
    if db.query(Pipeline).filter(Pipeline.name == body.name).first():
        raise HTTPException(400, "Pipeline exists")
    p = Pipeline(name=body.name, description=body.description)
    db.add(p); db.commit(); db.refresh(p)
    return p

@router.get("/", response_model=list[PipelineOut])
def list_pipelines(db: Session = Depends(get_db)):
    return db.query(Pipeline).order_by(Pipeline.name.asc()).all()
