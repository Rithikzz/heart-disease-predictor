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
        
        required_fields = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 
                           'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
        
        features = []
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
            try:
                features.append(float(data[field]))
            except ValueError:
                return jsonify({'error': f'Invalid value for field: {field}, must be numeric'}), 400
        
        features_array = np.array(features).reshape(1, -1)
        features_scaled = scaler.transform(features_array)
        
        prediction = model.predict(features_scaled)[0]
        probability = model.predict_proba(features_scaled)[0]
        
        # Optionally extracting feature importance to return
        # Just return top 3 contributing risk factors based on feature multiplied by model feature_importances_
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            # We skip detailed local interpretability for now, as global importance isn't patient-specific.
            # But we could just pass probabilities.

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
