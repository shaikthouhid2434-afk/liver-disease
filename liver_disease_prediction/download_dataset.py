"""
Download Indian Liver Patient Dataset from UCI ML Repository
Run this once before training: python download_dataset.py
"""

import urllib.request
import os

URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/00225/Indian%20Liver%20Patient%20Dataset%20(ILPD).csv"
DEST = "indian_liver_patient.csv"

if os.path.exists(DEST):
    print(f"Dataset already exists: {DEST}")
else:
    print("Downloading Indian Liver Patient Dataset...")
    try:
        urllib.request.urlretrieve(URL, DEST)
        print(f"✓ Dataset saved to: {DEST}")
    except Exception as e:
        print(f"Download failed: {e}")
        print("\nManual download instructions:")
        print("1. Visit: https://www.kaggle.com/datasets/uciml/indian-liver-patient-records")
        print("2. Download 'indian_liver_patient.csv'")
        print("3. Place it in this project folder")
