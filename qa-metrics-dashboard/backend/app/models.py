from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, ForeignKey, DateTime, Text, UniqueConstraint, Boolean
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(50), default="viewer")  # admin | viewer

class Pipeline(Base):
    __tablename__ = "pipelines"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text())
    metrics: Mapped[list["Metric"]] = relationship(back_populates="pipeline", cascade="all, delete-orphan")

class Metric(Base):
    __tablename__ = "metrics"
    id: Mapped[int] = mapped_column(primary_key=True)
    pipeline_id: Mapped[int] = mapped_column(ForeignKey("pipelines.id"))
    name: Mapped[str] = mapped_column(String(100))
    ts: Mapped[datetime] = mapped_column(DateTime, index=True)
    value: Mapped[float] = mapped_column(Float)
    pipeline: Mapped[Pipeline] = relationship(back_populates="metrics")
    __table_args__ = (UniqueConstraint("pipeline_id", "name", "ts", name="uix_metric_point"),)

class Anomaly(Base):
    __tablename__ = "anomalies"
    id: Mapped[int] = mapped_column(primary_key=True)
    metric_id: Mapped[int] = mapped_column(ForeignKey("metrics.id"), index=True)
    score: Mapped[float] = mapped_column(Float)
    is_anomaly: Mapped[bool] = mapped_column(Boolean, default=True)
    detected_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
