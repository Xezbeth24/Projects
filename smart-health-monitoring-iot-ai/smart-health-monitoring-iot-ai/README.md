# Smart Health Monitoring System (IoT + AI)

End-to-end system:
- **Device** (Arduino sketch) publishes vitals (heart rate, SpO2, temperature).
- **Server** (FastAPI + SQLite) ingests data and runs an ML risk model.
- **Dashboard** (Streamlit) visualizes live vitals and risk.
- **Simulator** can generate synthetic vitals if you don’t have hardware.

## Architecture
Device → REST (FastAPI) → SQLite → Streamlit dashboard  
ML: Logistic Regression risk of anomaly from vitals

## Quickstart (no hardware)
```bash
# 1) Create a venv and install
cd server
pip install -r requirements.txt
# train a simple model on synthetic data
python model_train.py
# run server
uvicorn app:app --reload --port 8000

# 2) In another shell, start simulator to send data
cd ../simulator
python send_data.py

# 3) Run dashboard
cd ../dashboard
streamlit run app.py
```

Server runs at http://localhost:8000, dashboard at the URL Streamlit prints.
