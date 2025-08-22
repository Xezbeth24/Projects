from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import sqlite3, os, joblib
import numpy as np

DB_PATH = os.path.join(os.path.dirname(__file__), "health.db")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

app = FastAPI(title="Health Ingest + Risk API")

class Vitals(BaseModel):
  device_id: str
  heart_rate: float
  spo2: float
  temperature: float
  ts: float | None = None

def init_db():
  with sqlite3.connect(DB_PATH) as con:
    con.execute(
      "CREATE TABLE IF NOT EXISTS vitals (id INTEGER PRIMARY KEY AUTOINCREMENT, device_id TEXT, heart_rate REAL, spo2 REAL, temperature REAL, risk REAL, ts TEXT)"
    )
    con.commit()

init_db()

def load_model():
  if os.path.exists(MODEL_PATH):
    return joblib.load(MODEL_PATH)
  return None

model = load_model()

@app.get("/health")
def health():
  return {"ok": True}

@app.post("/ingest")
def ingest(v: Vitals):
  global model
  ts = v.ts or datetime.utcnow().timestamp()
  features = np.array([[v.heart_rate, v.spo2, v.temperature]])
  risk = 0.0
  if model is not None:
    risk = float(model.predict_proba(features)[0,1])
  with sqlite3.connect(DB_PATH) as con:
    con.execute(
      "INSERT INTO vitals (device_id,heart_rate,spo2,temperature,risk,ts) VALUES (?,?,?,?,?,?)",
      (v.device_id, v.heart_rate, v.spo2, v.temperature, risk, datetime.utcfromtimestamp(ts).isoformat())
    )
    con.commit()
  return {"status": "ok", "risk": risk}

@app.get("/latest")
def latest(limit: int = 50):
  with sqlite3.connect(DB_PATH) as con:
    cur = con.execute("SELECT device_id, heart_rate, spo2, temperature, risk, ts FROM vitals ORDER BY id DESC LIMIT ?", (limit,))
    rows = [dict(zip([c[0] for c in cur.description], r)) for r in cur.fetchall()]
  return {"data": rows}
