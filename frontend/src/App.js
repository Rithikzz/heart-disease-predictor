import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const STEPS = [
  {
    id: 'age',
    label: 'How old are you?',
    description: 'Enter your current age in years.',
    icon: '🎂',
    category: 'Personal Info',
    type: 'number',
    placeholder: '45',
    unit: 'Years',
    min: 1,
    max: 120,
  },
  {
    id: 'sex',
    label: 'What is your biological sex?',
    description: 'Select as recorded in your medical records.',
    icon: '🧬',
    category: 'Personal Info',
    type: 'select',
    options: [
      { value: '1', label: 'Male', emoji: '♂️' },
      { value: '0', label: 'Female', emoji: '♀️' },
    ],
  },
  {
    id: 'cp',
    label: 'Chest Pain Type',
    description: 'What type of chest pain have you experienced?',
    icon: '💢',
    category: 'Symptoms',
    type: 'select',
    options: [
      { value: '0', label: 'Typical Angina', sub: 'Chest pain due to heart', emoji: '🫀' },
      { value: '1', label: 'Atypical Angina', sub: 'Chest pain not from heart', emoji: '⚡' },
      { value: '2', label: 'Non-anginal Pain', sub: 'Non-cardiac chest pain', emoji: '🌡️' },
      { value: '3', label: 'Asymptomatic', sub: 'No chest pain at all', emoji: '✨' },
    ],
  },
  {
    id: 'trestbps',
    label: 'Resting Blood Pressure',
    description: 'Your blood pressure measured while at rest.',
    icon: '🩺',
    category: 'Vitals',
    type: 'number',
    placeholder: '120',
    unit: 'mm Hg',
    min: 50,
    max: 250,
  },
  {
    id: 'chol',
    label: 'Serum Cholesterol',
    description: 'Total cholesterol level from your blood test.',
    icon: '🧪',
    category: 'Vitals',
    type: 'number',
    placeholder: '200',
    unit: 'mg/dl',
    min: 100,
    max: 600,
  },
  {
    id: 'fbs',
    label: 'Fasting Blood Sugar',
    description: 'Is your fasting blood sugar greater than 120 mg/dl?',
    icon: '🍬',
    category: 'Vitals',
    type: 'select',
    options: [
      { value: '0', label: 'No', sub: '≤ 120 mg/dl (Normal)', emoji: '✅' },
      { value: '1', label: 'Yes', sub: '> 120 mg/dl (Elevated)', emoji: '⚠️' },
    ],
  },
  {
    id: 'restecg',
    label: 'Resting ECG Results',
    description: 'Results from your resting electrocardiogram.',
    icon: '📈',
    category: 'Diagnostics',
    type: 'select',
    options: [
      { value: '0', label: 'Normal', sub: 'No irregularities detected', emoji: '💚' },
      { value: '1', label: 'ST-T Wave Abnormality', sub: 'T wave changes or ST deviation', emoji: '🟡' },
      { value: '2', label: 'Left Ventricular Hypertrophy', sub: 'Enlarged heart muscle', emoji: '🔴' },
    ],
  },
  {
    id: 'thalach',
    label: 'Maximum Heart Rate',
    description: 'Highest heart rate reached during a stress test.',
    icon: '❤️‍🔥',
    category: 'Vitals',
    type: 'number',
    placeholder: '150',
    unit: 'bpm',
    min: 60,
    max: 220,
  },
  {
    id: 'exang',
    label: 'Exercise-Induced Angina',
    description: 'Did you experience chest pain triggered by exercise?',
    icon: '🏃',
    category: 'Symptoms',
    type: 'select',
    options: [
      { value: '0', label: 'No', sub: 'No chest pain during exercise', emoji: '✅' },
      { value: '1', label: 'Yes', sub: 'Chest pain triggered by exercise', emoji: '⚠️' },
    ],
  },
  {
    id: 'oldpeak',
    label: 'ST Depression (Oldpeak)',
    description: 'ST depression induced by exercise relative to rest.',
    icon: '📉',
    category: 'Diagnostics',
    type: 'number',
    placeholder: '1.5',
    unit: 'mm',
    step: '0.1',
    min: 0,
    max: 10,
  },
  {
    id: 'slope',
    label: 'Slope of Peak Exercise ST',
    description: 'Shape of the ST segment at peak exercise.',
    icon: '📊',
    category: 'Diagnostics',
    type: 'select',
    options: [
      { value: '0', label: 'Upsloping', sub: 'Better rate with exercise', emoji: '📈' },
      { value: '1', label: 'Flat', sub: 'Minimal slope change', emoji: '➡️' },
      { value: '2', label: 'Downsloping', sub: 'Indicates unhealthy heart', emoji: '📉' },
    ],
  },
  {
    id: 'ca',
    label: 'Major Vessels (Fluoroscopy)',
    description: 'Number of major blood vessels visible via fluoroscopy.',
    icon: '🔬',
    category: 'Diagnostics',
    type: 'select',
    options: [
      { value: '0', label: '0 vessels', sub: 'No vessels colored', emoji: '⚪' },
      { value: '1', label: '1 vessel', sub: 'One vessel colored', emoji: '🔵' },
      { value: '2', label: '2 vessels', sub: 'Two vessels colored', emoji: '🟣' },
      { value: '3', label: '3 vessels', sub: 'Three vessels colored', emoji: '🔴' },
    ],
  },
  {
    id: 'thal',
    label: 'Thalassemia',
    description: 'A blood disorder affecting haemoglobin production.',
    icon: '🩸',
    category: 'Diagnostics',
    type: 'select',
    options: [
      { value: '3', label: 'Normal', sub: 'No thalassemia detected', emoji: '💚' },
      { value: '6', label: 'Fixed Defect', sub: 'Permanent heart defect', emoji: '🟡' },
      { value: '7', label: 'Reversible Defect', sub: 'Defect that can reverse', emoji: '🟠' },
    ],
  },
];

const DEFAULT_VALUES = {
  age: '',  sex: '1',  cp: '0',  trestbps: '',  chol: '',
  fbs: '0', restecg: '0', thalach: '', exang: '0', oldpeak: '',
  slope: '0', ca: '0', thal: '3',
};

function App() {
  const [formData, setFormData] = useState({ ...DEFAULT_VALUES });
  const [currentStep, setCurrentStep] = useState(0);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [direction, setDirection] = useState('forward');
  const [animKey, setAnimKey] = useState(0);
  const [pulse, setPulse] = useState(false);

  const totalSteps = STEPS.length;
  const step = STEPS[currentStep];
  const isLastStep = currentStep === totalSteps - 1;

  // Heartbeat pulse on mount
  useEffect(() => {
    const t = setInterval(() => setPulse(p => !p), 1500);
    return () => clearInterval(t);
  }, []);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const selectOption = (fieldId, value) => {
    setFormData({ ...formData, [fieldId]: value });
  };

  const handleNext = async () => {
    if (isLastStep) {
      await handleSubmit();
    } else {
      setDirection('forward');
      setAnimKey(k => k + 1);
      setCurrentStep(s => s + 1);
    }
  };

  const handleBack = () => {
    setDirection('back');
    setAnimKey(k => k + 1);
    setCurrentStep(s => s - 1);
  };

  const handleRestart = () => {
    setFormData({ ...DEFAULT_VALUES });
    setResult(null);
    setError(null);
    setCurrentStep(0);
    setDirection('forward');
    setAnimKey(k => k + 1);
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      await new Promise(r => setTimeout(r, 1000));
      const response = await axios.post('http://localhost:5000/api/predict', formData);
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to get prediction. Please try again.');
      setLoading(false);
    } finally {
      setLoading(false);
    }
  };

  const isCurrentFieldValid = () => {
    if (!step) return true;
    const val = formData[step.id];
    if (step.type === 'number') return val !== '' && !isNaN(Number(val)) && Number(val) > 0;
    return true;
  };

  const progress = ((currentStep + 1) / totalSteps) * 100;

  return (
    <div className="app-container">
      {/* Animated background */}
      <div className="bg-grid" />
      <div className="blob blob-1" />
      <div className="blob blob-2" />
      <div className="blob blob-3" />

      {/* Floating particles */}
      <div className="particles">
        {[...Array(8)].map((_, i) => (
          <div key={i} className={`particle particle-${i + 1}`} />
        ))}
      </div>

      <div className="glass-card">
        {/* Header */}
        <div className="header">
          <div className={`logo-wrap ${pulse ? 'pulse' : ''}`}>
            <span className="logo-icon">❤️</span>
          </div>
          <h1>Heart Guard <span className="brand-ai">AI</span></h1>
          <p className="subtitle">Advanced Cardiac Risk Assessment</p>
        </div>

        {/* ── Result Screen ── */}
        {result ? (
          <div className="result-screen">
            <div className={`result-card ${result.prediction === 1 ? 'high-risk' : 'low-risk'}`}>
              <div className="result-ring">
                <span className="result-emoji">{result.prediction === 1 ? '⚠️' : '✅'}</span>
              </div>
              <h2 className="result-title">
                {result.prediction === 1 ? 'Elevated Risk Detected' : 'Low Risk Indicated'}
              </h2>
              <div className="risk-badge-large">
                {result.prediction === 1 ? '⚡ CONSULT A DOCTOR' : '💚 LOOKING HEALTHY'}
              </div>

              <div className="prob-grid">
                <div className="prob-box healthy">
                  <div className="prob-label">Healthy Probability</div>
                  <div className="prob-value">{(result.probability.no_disease * 100).toFixed(1)}%</div>
                  <div className="prob-bar">
                    <div className="prob-fill healthy-fill" style={{ width: `${result.probability.no_disease * 100}%` }} />
                  </div>
                </div>
                <div className="prob-box disease">
                  <div className="prob-label">Disease Risk</div>
                  <div className="prob-value">{(result.probability.disease * 100).toFixed(1)}%</div>
                  <div className="prob-bar">
                    <div className="prob-fill disease-fill" style={{ width: `${result.probability.disease * 100}%` }} />
                  </div>
                </div>
              </div>

              <p className="disclaimer">
                ℹ️ This AI-powered prediction is for informational purposes only. Always consult a qualified medical professional for an accurate diagnosis.
              </p>
            </div>

            <button className="restart-btn" onClick={handleRestart}>
              🔄 Start New Assessment
            </button>
          </div>
        ) : (
          <>
            {/* ── Error ── */}
            {error && (
              <div className="error-banner">
                <span>⚠️</span>
                <div>
                  <strong>Connection Error</strong>
                  <p>{error}</p>
                </div>
              </div>
            )}

            {/* ── Progress ── */}
            <div className="progress-section">
              <div className="progress-meta">
                <span className="category-tag">{step.category}</span>
                <span className="step-count">{currentStep + 1} / {totalSteps}</span>
              </div>
              <div className="progress-track">
                <div className="progress-fill" style={{ width: `${progress}%` }} />
              </div>
              <div className="step-dots">
                {STEPS.map((s, i) => (
                  <div
                    key={i}
                    className={`step-dot ${i < currentStep ? 'done' : i === currentStep ? 'active' : ''}`}
                    title={s.label}
                  />
                ))}
              </div>
            </div>

            {/* ── Active Step ── */}
            <div className={`step-slide ${direction}`} key={animKey}>
              <div className="step-icon-wrap">
                <span className="step-icon">{step.icon}</span>
              </div>

              <div className="step-text">
                <h2>{step.label}</h2>
                <p>{step.description}</p>
              </div>

              <div className="input-area">
                {step.type === 'number' ? (
                  <div className="num-field">
                    <input
                      type="number"
                      name={step.id}
                      value={formData[step.id]}
                      onChange={handleChange}
                      placeholder={step.placeholder}
                      min={step.min}
                      max={step.max}
                      step={step.step || '1'}
                      className="big-num-input"
                      autoFocus
                    />
                    {step.unit && <div className="unit-chip">{step.unit}</div>}
                  </div>
                ) : (
                  <div className="opt-grid" data-count={step.options.length}>
                    {step.options.map(opt => (
                      <button
                        key={opt.value}
                        type="button"
                        className={`opt-btn ${formData[step.id] === opt.value ? 'selected' : ''}`}
                        onClick={() => selectOption(step.id, opt.value)}
                      >
                        <span className="opt-emoji">{opt.emoji}</span>
                        <span className="opt-main">{opt.label}</span>
                        {opt.sub && <span className="opt-sub">{opt.sub}</span>}
                        {formData[step.id] === opt.value && <span className="opt-check">✓</span>}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            </div>

            {/* ── Navigation ── */}
            <div className="nav-row">
              {currentStep > 0 ? (
                <button className="back-btn" onClick={handleBack} type="button">
                  <span>←</span> Back
                </button>
              ) : (
                <div />
              )}

              <button
                className={`next-btn ${loading ? 'loading' : ''} ${isLastStep ? 'submit' : ''}`}
                onClick={handleNext}
                disabled={loading || !isCurrentFieldValid()}
                type="button"
              >
                {loading ? (
                  <span className="spinner" />
                ) : isLastStep ? (
                  <><span>🔍</span> Analyze Now</>
                ) : (
                  <>Continue <span>→</span></>
                )}
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default App;