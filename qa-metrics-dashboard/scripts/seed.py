import csv
import os
from datetime import datetime
import requests

API = os.getenv("API", "http://localhost:8000")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@example.com")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Admin@12345")

# 1) init DB and users
requests.post(f"{API}/auth/init")
# 2) login
r = requests.post(f"{API}/auth/token", json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD})
r.raise_for_status()
token = r.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}
# 3) ingest CSV points
pts = []
with open(os.path.join(os.path.dirname(__file__), "seed_metrics.csv")) as f:
    for row in csv.DictReader(f):
        pts.append({
            "pipeline": row["pipeline"],
            "name": row["name"],
            "ts": row["ts"],
            "value": float(row["value"])
        })
requests.post(f"{API}/metrics/ingest", json=pts, headers=headers).raise_for_status()
print("Seeded", len(pts), "points")
