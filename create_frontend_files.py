import os

# Create frontend directories if they don't exist
os.makedirs('frontend/public', exist_ok=True)
os.makedirs('frontend/src', exist_ok=True)

# package.json
package_json = '''{
  "name": "heart-disease-predictor",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "@testing-library/jest-dom": "^5.17.0",
    "@testing-library/react": "^13.4.0",
    "@testing-library/user-event": "^13.5.0",
    "axios": "^1.6.2",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": [
      "react-app",
      "react-app/jest"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  },
  "proxy": "http://localhost:5000"
}'''

# index.html
index_html = '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="Heart Disease Prediction App" />
    <title>Heart Disease Predictor</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>'''

# index.js
index_js = '''import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);'''

# index.css
index_css = '''* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New',
    monospace;
}'''

# App.js
app_js = '''import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [formData, setFormData] = useState({
    age: '',
    sex: '1',
    cp: '0',
    trestbps: '',
    chol: '',
    fbs: '0',
    restecg: '0',
    thalach: '',
    exang: '0',
    oldpeak: '',
    slope: '0',
    ca: '0',
    thal: '0'
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post('http://localhost:5000/api/predict', formData);
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to get prediction. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="container">
        <h1>❤️ Heart Disease Predictor</h1>
        <p className="subtitle">Enter patient information to predict heart disease risk</p>

        <form onSubmit={handleSubmit} className="prediction-form">
          <div className="form-grid">
            <div className="form-group">
              <label>Age</label>
              <input
                type="number"
                name="age"
                value={formData.age}
                onChange={handleChange}
                required
                placeholder="e.g., 45"
              />
            </div>

            <div className="form-group">
              <label>Sex</label>
              <select name="sex" value={formData.sex} onChange={handleChange}>
                <option value="1">Male</option>
                <option value="0">Female</option>
              </select>
            </div>

            <div className="form-group">
              <label>Chest Pain Type (cp)</label>
              <select name="cp" value={formData.cp} onChange={handleChange}>
                <option value="0">Typical Angina</option>
                <option value="1">Atypical Angina</option>
                <option value="2">Non-anginal Pain</option>
                <option value="3">Asymptomatic</option>
              </select>
            </div>

            <div className="form-group">
              <label>Resting Blood Pressure (mm Hg)</label>
              <input
                type="number"
                name="trestbps"
                value={formData.trestbps}
                onChange={handleChange}
                required
                placeholder="e.g., 120"
              />
            </div>

            <div className="form-group">
              <label>Serum Cholesterol (mg/dl)</label>
              <input
                type="number"
                name="chol"
                value={formData.chol}
                onChange={handleChange}
                required
                placeholder="e.g., 200"
              />
            </div>

            <div className="form-group">
              <label>Fasting Blood Sugar &gt; 120 mg/dl</label>
              <select name="fbs" value={formData.fbs} onChange={handleChange}>
                <option value="0">No</option>
                <option value="1">Yes</option>
              </select>
            </div>

            <div className="form-group">
              <label>Resting ECG Results</label>
              <select name="restecg" value={formData.restecg} onChange={handleChange}>
                <option value="0">Normal</option>
                <option value="1">ST-T Wave Abnormality</option>
                <option value="2">Left Ventricular Hypertrophy</option>
              </select>
            </div>

            <div className="form-group">
              <label>Max Heart Rate Achieved</label>
              <input
                type="number"
                name="thalach"
                value={formData.thalach}
                onChange={handleChange}
                required
                placeholder="e.g., 150"
              />
            </div>

            <div className="form-group">
              <label>Exercise Induced Angina</label>
              <select name="exang" value={formData.exang} onChange={handleChange}>
                <option value="0">No</option>
                <option value="1">Yes</option>
              </select>
            </div>

            <div className="form-group">
              <label>ST Depression (oldpeak)</label>
              <input
                type="number"
                step="0.1"
                name="oldpeak"
                value={formData.oldpeak}
                onChange={handleChange}
                required
                placeholder="e.g., 1.5"
              />
            </div>

            <div className="form-group">
              <label>Slope of Peak Exercise ST</label>
              <select name="slope" value={formData.slope} onChange={handleChange}>
                <option value="0">Upsloping</option>
                <option value="1">Flat</option>
                <option value="2">Downsloping</option>
              </select>
            </div>

            <div className="form-group">
              <label>Number of Major Vessels (ca)</label>
              <select name="ca" value={formData.ca} onChange={handleChange}>
                <option value="0">0</option>
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
              </select>
            </div>

            <div className="form-group">
              <label>Thalassemia (thal)</label>
              <select name="thal" value={formData.thal} onChange={handleChange}>
                <option value="0">Normal</option>
                <option value="1">Fixed Defect</option>
                <option value="2">Reversible Defect</option>
              </select>
            </div>
          </div>

          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? 'Analyzing...' : 'Predict'}
          </button>
        </form>

        {error && (
          <div className="result error">
            <h2>Error</h2>
            <p>{error}</p>
          </div>
        )}

        {result && (
          <div className={`result ${result.prediction === 1 ? 'high-risk' : 'low-risk'}`}>
            <h2>Prediction Result</h2>
            <div className="result-content">
              <div className="risk-badge">{result.risk}</div>
              <div className="probabilities">
                <div className="prob-item">
                  <span className="prob-label">No Disease:</span>
                  <span className="prob-value">{(result.probability.no_disease * 100).toFixed(2)}%</span>
                </div>
                <div className="prob-item">
                  <span className="prob-label">Disease:</span>
                  <span className="prob-value">{(result.probability.disease * 100).toFixed(2)}%</span>
                </div>
              </div>
            </div>
            <p className="disclaimer">
              ⚠️ This is a prediction tool and should not replace professional medical advice.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;'''

# App.css
app_css = '''.App {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.container {
  background: white;
  border-radius: 20px;
  padding: 40px;
  max-width: 900px;
  width: 100%;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

h1 {
  text-align: center;
  color: #667eea;
  font-size: 2.5rem;
  margin-bottom: 10px;
}

.subtitle {
  text-align: center;
  color: #666;
  margin-bottom: 30px;
  font-size: 1.1rem;
}

.prediction-form {
  margin-bottom: 30px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 8px;
  color: #333;
  font-weight: 600;
  font-size: 0.9rem;
}

.form-group input,
.form-group select {
  padding: 12px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #667eea;
}

.submit-btn {
  width: 100%;
  padding: 15px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1.2rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.result {
  padding: 30px;
  border-radius: 15px;
  margin-top: 30px;
  animation: slideIn 0.5s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.result.low-risk {
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
  color: white;
}

.result.high-risk {
  background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
  color: white;
}

.result.error {
  background: #ffebee;
  color: #c62828;
  border: 2px solid #c62828;
}

.result h2 {
  margin-bottom: 20px;
  font-size: 1.8rem;
}

.result-content {
  margin-bottom: 20px;
}

.risk-badge {
  display: inline-block;
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 25px;
  font-size: 1.3rem;
  font-weight: 700;
  margin-bottom: 20px;
}

.probabilities {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.prob-item {
  flex: 1;
  min-width: 200px;
  background: rgba(255, 255, 255, 0.2);
  padding: 15px;
  border-radius: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.prob-label {
  font-weight: 600;
}

.prob-value {
  font-size: 1.2rem;
  font-weight: 700;
}

.disclaimer {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 2px solid rgba(255, 255, 255, 0.3);
  font-size: 0.9rem;
  text-align: center;
}

@media (max-width: 768px) {
  .container {
    padding: 20px;
  }

  h1 {
    font-size: 2rem;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }
}'''

# Write all files
with open('frontend/package.json', 'w', encoding='utf-8') as f:
    f.write(package_json)

with open('frontend/public/index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)

with open('frontend/src/index.js', 'w', encoding='utf-8') as f:
    f.write(index_js)

with open('frontend/src/index.css', 'w', encoding='utf-8') as f:
    f.write(index_css)

with open('frontend/src/App.js', 'w', encoding='utf-8') as f:
    f.write(app_js)

with open('frontend/src/App.css', 'w', encoding='utf-8') as f:
    f.write(app_css)

print("✅ Frontend files created successfully!")
print("\nFiles created:")
print("  - frontend/package.json")
print("  - frontend/public/index.html")
print("  - frontend/src/index.js")
print("  - frontend/src/index.css")
print("  - frontend/src/App.js")
print("  - frontend/src/App.css")
print("\nNext steps:")
print("  1. cd frontend")
print("  2. npm install")
print("  3. npm start")
