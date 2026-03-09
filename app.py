from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Flask backend is running"

try:
    model = joblib.load('heart_disease_model.pkl')
    scaler = joblib.load('scaler.pkl')
    model_loaded = True
except:
    model_loaded = False
    print("Warning: Model files not found. Please train the model first.")

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'running',
        'model_loaded': model_loaded
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    if not model_loaded:
        return jsonify({'error': 'Model not loaded. Please train the model first.'}), 500
    
    try:
        data = request.json
        
        features = [
            float(data['age']),
            float(data['sex']),
            float(data['cp']),
            float(data['trestbps']),
            float(data['chol']),
            float(data['fbs']),
            float(data['restecg']),
            float(data['thalach']),
            float(data['exang']),
            float(data['oldpeak']),
            float(data['slope']),
            float(data['ca']),
            float(data['thal'])
        ]
        
        features_array = np.array(features).reshape(1, -1)
        features_scaled = scaler.transform(features_array)
        
        prediction = model.predict(features_scaled)[0]
        probability = model.predict_proba(features_scaled)[0]
        
        result = {
            'prediction': int(prediction),
            'risk': 'High Risk' if prediction == 1 else 'Low Risk',
            'probability': {
                'no_disease': float(probability[0]),
                'disease': float(probability[1])
            }
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
