import pandas as pd
from sqlalchemy.orm import Session
from sklearn.ensemble import IsolationForest
from ..models import Metric, Pipeline, Anomaly

class AnomalyService:
    def __init__(self, db: Session):
        self.db = db

    def detect_for(self, pipeline: str, name: str, contamination: float = 0.1, n_estimators: int = 100):
        q = (
            self.db.query(Metric)
            .join(Pipeline, Pipeline.id == Metric.pipeline_id)
            .filter(Pipeline.name == pipeline, Metric.name == name)
            .order_by(Metric.ts.asc())
        )
        rows = q.all()
        if not rows:
            return []
        df = pd.DataFrame([{ "ts": r.ts, "value": r.value, "id": r.id } for r in rows])
        model = IsolationForest(contamination=contamination, n_estimators=n_estimators, random_state=42)
        preds = model.fit_predict(df[["value"]])
        scores = model.decision_function(df[["value"]])
        out = []
        for (_, r), y, s in zip(df.iterrows(), preds, scores):
            if y == -1:
                out.append({"metric_id": int(r["id"]), "ts": r["ts"], "value": float(r["value"]), "score": float(s)})
        # Simple refresh strategy for demo
        self.db.query(Anomaly).filter(Anomaly.metric_id.in_(df["id"].tolist())).delete(synchronize_session=False)
        for a in out:
            self.db.add(Anomaly(metric_id=a["metric_id"], score=a["score"], is_anomaly=True))
        self.db.commit()
        return out
