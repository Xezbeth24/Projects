import numpy as np, os, joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

# Synthetic data: normal vs. anomalous
np.random.seed(42)
n = 2000
hr = np.random.normal(80, 12, n)
spo2 = np.random.normal(97, 1.2, n)
temp = np.random.normal(37.0, 0.5, n)
# anomalies: high temp or low spo2 or very high/low hr
y = ((temp > 38.0) | (spo2 < 95) | (hr > 110) | (hr < 50)).astype(int)

X = np.column_stack([hr, spo2, temp])
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=42)
clf = LogisticRegression()
clf.fit(Xtr, ytr)
print("Train score:", clf.score(Xtr, ytr), "Test score:", clf.score(Xte, yte))
joblib.dump(clf, MODEL_PATH)
print("Saved", MODEL_PATH)
