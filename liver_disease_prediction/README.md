# 🩺 Liver Disease Prediction Using Ensemble Models

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.3-green)
![ML](https://img.shields.io/badge/ML-Ensemble%20Models-orange)
![Dataset](https://img.shields.io/badge/Dataset-ILPD-red)

An AI-powered full-stack web application that predicts liver disease using an Ensemble of Machine Learning models trained on the **Indian Liver Patient Dataset (ILPD)**.

---

## 📁 Project Structure

```
liver_disease_prediction/
│
├── app.py                    # Flask backend
├── train_model.py            # ML model training script
├── download_dataset.py       # Dataset downloader
├── requirements.txt          # Python dependencies
├── indian_liver_patient.csv  # Dataset (download separately)
│
├── model/
│   ├── model.pkl             # Saved Voting Classifier
│   └── scaler.pkl            # Saved StandardScaler
│
├── templates/
│   ├── index.html            # Main prediction form
│   └── result.html           # Prediction result page
│
└── static/
    ├── css/
    │   └── style.css         # Medical-themed styles
    └── js/
        └── main.js           # Frontend JavaScript
```

---

## 🧠 ML Models Used

| Model                 | Type          |
|-----------------------|---------------|
| Logistic Regression   | Linear        |
| Random Forest         | Tree Ensemble |
| XGBoost               | Boosting      |
| AdaBoost              | Boosting      |
| **Voting Classifier** | **Ensemble**  |

The **Voting Classifier** uses soft voting across all 4 models for maximum accuracy.

---

## 📊 Dataset Features

| Feature                    | Description                  | Unit    |
|----------------------------|------------------------------|---------|
| Age                        | Patient age                  | Years   |
| Gender                     | Male / Female                | —       |
| Total Bilirubin             | Liver function test          | mg/dL   |
| Direct Bilirubin            | Liver function test          | mg/dL   |
| Alkaline Phosphotase        | Enzyme level                 | IU/L    |
| Alamine Aminotransferase    | ALT enzyme level             | U/L     |
| Aspartate Aminotransferase  | AST enzyme level             | U/L     |
| Total Proteins              | Protein levels               | g/dL    |
| Albumin                     | Protein in blood             | g/dL    |
| Albumin/Globulin Ratio      | Ratio of proteins            | —       |

---

## 🚀 Setup & Run (Step by Step)

### Step 1: Clone / Download the project
```bash
git clone https://github.com/yourusername/liver-disease-prediction.git
cd liver_disease_prediction
```

### Step 2: Create a virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Download the dataset
```bash
python download_dataset.py
```
> If auto-download fails, manually download `indian_liver_patient.csv` from:
> https://www.kaggle.com/datasets/uciml/indian-liver-patient-records
> and place it in the project root folder.

### Step 5: Train the model
```bash
python train_model.py
```
This will create `model/model.pkl` and `model/scaler.pkl`.

### Step 6: Run the Flask app
```bash
python app.py
```

### Step 7: Open in browser
```
http://localhost:5000
```

---

## 🌐 API Usage (JSON endpoint)

```bash
POST /api/predict
Content-Type: application/json

{
  "age": 45,
  "gender": "Male",
  "total_bilirubin": 0.9,
  "direct_bilirubin": 0.3,
  "alkaline_phosphotase": 187,
  "alamine_aminotransferase": 16,
  "aspartate_aminotransferase": 18,
  "total_proteins": 6.8,
  "albumin": 3.3,
  "albumin_globulin_ratio": 0.9
}
```

**Response:**
```json
{
  "success": true,
  "prediction": 1,
  "label": "Liver Disease Detected",
  "confidence": 78.5
}
```

---

## ⚠️ Disclaimer

> This tool is built for **educational and research purposes only**.
> It is **not a substitute** for professional medical diagnosis or treatment.
> Always consult a qualified healthcare professional.

---

## 📄 License

MIT License — Free to use, modify, and distribute.
