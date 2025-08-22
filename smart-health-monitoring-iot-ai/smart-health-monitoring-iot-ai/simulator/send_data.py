import time, random, requests

BASE = "http://localhost:8000"

def sample():
  hr = random.gauss(80, 10)
  spo2 = random.gauss(97, 1.0)
  temp = random.gauss(37.0, 0.4)
  # randomly create anomalies
  if random.random() < 0.1:
    temp += random.uniform(1.0, 2.0)
  if random.random() < 0.1:
    spo2 -= random.uniform(2.0, 4.0)
  if random.random() < 0.1:
    hr += random.uniform(25.0, 40.0)
  return dict(device_id="sim-001", heart_rate=hr, spo2=spo2, temperature=temp)

if __name__ == "__main__":
  print("Sending synthetic vitals to server. Ctrl+C to stop.")
  while True:
    data = sample()
    try:
      r = requests.post(f"{BASE}/ingest", json=data, timeout=5)
      print("POST", data, "->", r.status_code, r.json())
    except Exception as e:
      print("Error:", e)
    time.sleep(2)
