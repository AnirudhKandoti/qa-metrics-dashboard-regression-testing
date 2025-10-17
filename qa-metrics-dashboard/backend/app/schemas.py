from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str = "viewer"

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str

    class Config:
        from_attributes = True

class PipelineCreate(BaseModel):
    name: str
    description: str | None = None

class PipelineOut(BaseModel):
    id: int
    name: str
    description: str | None = None

    class Config:
        from_attributes = True

class MetricPoint(BaseModel):
    pipeline: str
    name: str
    ts: datetime
    value: float

class MetricSeriesQuery(BaseModel):
    pipeline: str
    name: str
    since: datetime | None = None
    until: datetime | None = None

class MetricSeriesPoint(BaseModel):
    ts: datetime
    value: float

class MetricSeriesOut(BaseModel):
    pipeline: str
    name: str
    points: List[MetricSeriesPoint]

class AnomalyOut(BaseModel):
    ts: datetime
    value: float
    score: float
