import requests, time, pandas as pd, streamlit as st

st.set_page_config(page_title="Health Monitor", page_icon="🩺", layout="wide")
st.title("🩺 Smart Health Monitoring Dashboard")

api = st.sidebar.text_input("API base URL", "http://localhost:8000")
refresh = st.sidebar.number_input("Refresh seconds", 1, 30, 3)

placeholder = st.empty()

def load_latest():
  try:
    r = requests.get(f"{api}/latest?limit=100")
    r.raise_for_status()
    return pd.DataFrame(r.json().get("data", []))
  except Exception as e:
    st.error(f"Failed to load: {e}")
    return pd.DataFrame()

while True:
  df = load_latest()
  with placeholder.container():
    if df.empty:
      st.info("No data yet. Start the simulator or post to /ingest.")
    else:
      st.dataframe(df.tail(20), use_container_width=True)
      col1, col2, col3 = st.columns(3)
      with col1:
        st.metric("Latest HR", f"{df.iloc[0]['heart_rate']:.0f} bpm")
      with col2:
        st.metric("Latest SpO2", f"{df.iloc[0]['spo2']:.0f} %")
      with col3:
        st.metric("Risk", f"{df.iloc[0]['risk']:.2f}")
      try:
        df_sorted = df.sort_values('ts')
        st.line_chart(df_sorted[['heart_rate','spo2','temperature']])
      except Exception:
        pass
  time.sleep(refresh)
