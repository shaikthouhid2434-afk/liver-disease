"""
Liver Disease Prediction - Model Training Script
Uses Indian Liver Patient Dataset (ILPD)
"""

import pandas as pd
import numpy as np
import pickle
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, VotingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from xgboost import XGBClassifier

# ─────────────────────────────────────────────
# 1. LOAD DATASET
# ─────────────────────────────────────────────
print("=" * 60)
print("  LIVER DISEASE PREDICTION - MODEL TRAINING")
print("=" * 60)

# Column names for ILPD dataset
columns = [
    'Age', 'Gender', 'Total_Bilirubin', 'Direct_Bilirubin',
    'Alkaline_Phosphotase', 'Alamine_Aminotransferase',
    'Aspartate_Aminotransferase', 'Total_Proteins',
    'Albumin', 'Albumin_and_Globulin_Ratio', 'Dataset'
]

# Load dataset
print("\n[1/6] Loading Dataset...")
df = pd.read_csv('indian_liver_patient.csv', names=columns)
print(f"      Shape: {df.shape}")
print(f"      Disease cases: {(df['Dataset'] == 1).sum()} | Healthy: {(df['Dataset'] == 2).sum()}")

# ─────────────────────────────────────────────
# 2. DATA PREPROCESSING
# ─────────────────────────────────────────────
print("\n[2/6] Preprocessing Data...")

# Encode Gender
le = LabelEncoder()
df['Gender'] = le.fit_transform(df['Gender'])  # Male=1, Female=0

# Handle missing values
df['Albumin_and_Globulin_Ratio'].fillna(df['Albumin_and_Globulin_Ratio'].median(), inplace=True)

# Convert target: 1 = Liver Disease, 0 = No Disease
df['Dataset'] = df['Dataset'].map({1: 1, 2: 0})

# Features and Target
X = df.drop('Dataset', axis=1)
y = df['Dataset']

print(f"      Missing values after cleaning: {X.isnull().sum().sum()}")
print(f"      Features: {list(X.columns)}")

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Feature Scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

print(f"      Train: {X_train.shape} | Test: {X_test.shape}")

# ─────────────────────────────────────────────
# 3. TRAIN INDIVIDUAL MODELS
# ─────────────────────────────────────────────
print("\n[3/6] Training Models...")

models = {
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'Random Forest':       RandomForestClassifier(n_estimators=100, random_state=42),
    'XGBoost':             XGBClassifier(n_estimators=100, random_state=42, eval_metric='logloss'),
    'AdaBoost':            AdaBoostClassifier(n_estimators=100, random_state=42),
}

results = {}
for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    results[name] = {
        'Accuracy':  round(accuracy_score(y_test, y_pred) * 100, 2),
        'Precision': round(precision_score(y_test, y_pred, zero_division=0) * 100, 2),
        'Recall':    round(recall_score(y_test, y_pred, zero_division=0) * 100, 2),
        'F1-Score':  round(f1_score(y_test, y_pred, zero_division=0) * 100, 2),
    }
    print(f"      ✓ {name} — Accuracy: {results[name]['Accuracy']}%")

# ─────────────────────────────────────────────
# 4. VOTING CLASSIFIER (ENSEMBLE)
# ─────────────────────────────────────────────
print("\n[4/6] Training Voting Classifier (Ensemble)...")

voting_clf = VotingClassifier(
    estimators=[
        ('lr',  LogisticRegression(max_iter=1000, random_state=42)),
        ('rf',  RandomForestClassifier(n_estimators=100, random_state=42)),
        ('xgb', XGBClassifier(n_estimators=100, random_state=42, eval_metric='logloss')),
        ('ada', AdaBoostClassifier(n_estimators=100, random_state=42)),
    ],
    voting='soft'
)
voting_clf.fit(X_train_scaled, y_train)
y_pred_vc = voting_clf.predict(X_test_scaled)

results['Voting Classifier'] = {
    'Accuracy':  round(accuracy_score(y_test, y_pred_vc) * 100, 2),
    'Precision': round(precision_score(y_test, y_pred_vc, zero_division=0) * 100, 2),
    'Recall':    round(recall_score(y_test, y_pred_vc, zero_division=0) * 100, 2),
    'F1-Score':  round(f1_score(y_test, y_pred_vc, zero_division=0) * 100, 2),
}
print(f"      ✓ Voting Classifier — Accuracy: {results['Voting Classifier']['Accuracy']}%")

# ─────────────────────────────────────────────
# 5. COMPARE MODELS
# ─────────────────────────────────────────────
print("\n[5/6] Model Comparison Report:")
print("-" * 65)
print(f"{'Model':<25} {'Accuracy':>10} {'Precision':>10} {'Recall':>10} {'F1-Score':>10}")
print("-" * 65)
for name, metrics in results.items():
    print(f"{name:<25} {metrics['Accuracy']:>9}% {metrics['Precision']:>9}% {metrics['Recall']:>9}% {metrics['F1-Score']:>9}%")
print("-" * 65)

# Detailed report for Voting Classifier
print("\nDetailed Classification Report (Voting Classifier):")
print(classification_report(y_test, y_pred_vc, target_names=['No Disease', 'Liver Disease']))

# ─────────────────────────────────────────────
# 6. SAVE MODEL & SCALER
# ─────────────────────────────────────────────
print("[6/6] Saving Best Model (Voting Classifier)...")

with open('model/model.pkl', 'wb') as f:
    pickle.dump(voting_clf, f)

with open('model/scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

print("      ✓ model/model.pkl saved")
print("      ✓ model/scaler.pkl saved")
print("\n" + "=" * 60)
print("  TRAINING COMPLETE!")
print("=" * 60)
