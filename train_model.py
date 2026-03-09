"""
Training script to generate heart_disease_model.pkl and scaler.pkl
Uses the authentic UCI Heart Disease dataset (Cleveland).
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib
import warnings
warnings.filterwarnings('ignore')

print("🏥 Training Heart Disease Prediction Model with UCI Dataset...")
print("=" * 50)

# Fetch data from UCI Machine Learning Repository
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"
columns = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 
           'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'target']

try:
    df = pd.read_csv(url, names=columns, na_values='?')
    print("✓ Successfully loaded UCI Heart Disease dataset.")
except Exception as e:
    print(f"❌ Error loading dataset: {e}")
    exit(1)

# Handle missing data
print(f"Dataset shape before dropping NAs: {df.shape}")
df.dropna(inplace=True)
print(f"Dataset shape after dropping NAs: {df.shape}")

# In the original UCI dataset, 'target' indicates the presence (values 1,2,3,4) or absence (0) of heart disease.
# We map all > 0 to 1 to create a binary classification problem.
df['target'] = (df['target'] > 0).astype(int)

print(f"✓ Total samples: {len(df)}")
print(f"✓ Features: {len(df.columns) - 1}")
print(f"✓ Disease cases: {df['target'].sum()} | Healthy: {(df['target'] == 0).sum()}")
print()

# Prepare data
X = df.drop('target', axis=1)
y = df['target']

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"✓ Split: {len(X_train)} train | {len(X_test)} test")
print()

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("✓ Features scaled")
print()

# Train model
print("🔄 Training Random Forest Classifier...")
# Updated hyper-parameters to better fit a small dataset
model = RandomForestClassifier(n_estimators=150, max_depth=10, min_samples_split=5, random_state=42)
model.fit(X_train_scaled, y_train)

# Evaluate
train_pred = model.predict(X_train_scaled)
test_pred = model.predict(X_test_scaled)

train_score = accuracy_score(y_train, train_pred)
test_score = accuracy_score(y_test, test_pred)

print(f"✓ Training Accuracy: {train_score:.2%}")
print(f"✓ Testing Accuracy: {test_score:.2%}")
print()
print("📊 Classification Report (Test Data):")
print(classification_report(y_test, test_pred))
print("Confusion Matrix:")
print(confusion_matrix(y_test, test_pred))
print()

# Save model and scaler
joblib.dump(model, 'heart_disease_model.pkl')
joblib.dump(scaler, 'scaler.pkl')

print("=" * 50)
print("✅ Model trained successfully!")
print("✅ Saved: heart_disease_model.pkl")
print("✅ Saved: scaler.pkl")
print()
print("🚀 Now you can run: python app.py")
print("=" * 50)
