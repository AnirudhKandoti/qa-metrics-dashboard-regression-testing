from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .settings import settings
from .routers import users, pipelines, metrics, anomalies

app = FastAPI(title="QA Metrics Dashboard API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(pipelines.router)
app.include_router(metrics.router)
app.include_router(anomalies.router)

@app.get("/")
def root():
    return {"ok": True}
