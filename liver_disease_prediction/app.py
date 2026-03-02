"""
Liver Disease Prediction - Flask Backend
"""

from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import os

app = Flask(__name__)

# ── Load Model & Scaler ──────────────────────
MODEL_PATH  = os.path.join('model', 'model.pkl')
SCALER_PATH = os.path.join('model', 'scaler.pkl')

with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

with open(SCALER_PATH, 'rb') as f:
    scaler = pickle.load(f)

# ── Routes ───────────────────────────────────
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Collect form inputs
        features = [
            float(request.form['age']),
            1 if request.form['gender'] == 'Male' else 0,
            float(request.form['total_bilirubin']),
            float(request.form['direct_bilirubin']),
            float(request.form['alkaline_phosphotase']),
            float(request.form['alamine_aminotransferase']),
            float(request.form['aspartate_aminotransferase']),
            float(request.form['total_proteins']),
            float(request.form['albumin']),
            float(request.form['albumin_globulin_ratio']),
        ]

        # Scale & Predict
        features_array  = np.array(features).reshape(1, -1)
        features_scaled = scaler.transform(features_array)
        prediction      = model.predict(features_scaled)[0]
        probability     = model.predict_proba(features_scaled)[0]

        result = {
            'prediction': int(prediction),
            'label':      'Liver Disease Detected' if prediction == 1 else 'No Liver Disease',
            'confidence': round(float(max(probability)) * 100, 2),
            'disease_prob': round(float(probability[1]) * 100, 2),
            'healthy_prob': round(float(probability[0]) * 100, 2),
        }
        return render_template('result.html', result=result, inputs=request.form)

    except Exception as e:
        return render_template('index.html', error=f"Error: {str(e)}")


@app.route('/api/predict', methods=['POST'])
def api_predict():
    """JSON API endpoint for programmatic access"""
    try:
        data = request.get_json()
        features = [
            float(data['age']),
            1 if data['gender'] == 'Male' else 0,
            float(data['total_bilirubin']),
            float(data['direct_bilirubin']),
            float(data['alkaline_phosphotase']),
            float(data['alamine_aminotransferase']),
            float(data['aspartate_aminotransferase']),
            float(data['total_proteins']),
            float(data['albumin']),
            float(data['albumin_globulin_ratio']),
        ]
        features_array  = np.array(features).reshape(1, -1)
        features_scaled = scaler.transform(features_array)
        prediction      = model.predict(features_scaled)[0]
        probability     = model.predict_proba(features_scaled)[0]

        return jsonify({
            'success': True,
            'prediction': int(prediction),
            'label': 'Liver Disease Detected' if prediction == 1 else 'No Liver Disease',
            'confidence': round(float(max(probability)) * 100, 2),
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
