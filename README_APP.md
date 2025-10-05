# 🌌 Exoplanet Detection Web Application

A beautiful, modern web application for detecting exoplanets using machine learning (XGBoost) trained on NASA TESS mission data.

## 🚀 Features

- **Real-time Prediction**: Instant exoplanet detection using trained XGBoost model (95.34% AUC)
- **Beautiful UI**: Modern, responsive interface with dark space theme
- **Feature Groups**: Organized input fields by category (Transit, Orbital, Stellar, Planet properties)
- **Example Data**: Load real TESS observations with one click
- **Confidence Scores**: View prediction probabilities and confidence metrics
- **Easy to Use**: Simple REST API and intuitive web interface

## 📋 Requirements

- Python 3.8+
- Trained models in `models/` directory:
  - `xgb_model.pkl` - XGBoost model
  - `scaler.pkl` - Feature scaler
  - `feature_names.pkl` - Feature metadata

## 🔧 Installation

1. **Activate your virtual environment** (if not already activated):
   ```bash
   # Windows
   tess_venv\Scripts\activate
   
   # Linux/Mac
   source tess_venv/bin/activate
   ```

2. **Install additional dependencies**:
   ```bash
   pip install flask flask-cors
   ```

   Or install all requirements:
   ```bash
   pip install -r requirements.txt
   ```

## 🏃 Running the Application

1. **Start the Flask server**:
   ```bash
   python app.py
   ```

2. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

3. **Use the application**:
   - Click "Load Example" to populate with real TESS data
   - Or manually enter observation values
   - Click "Detect Exoplanet" to get prediction
   - View results with confidence scores

## 🛠️ API Endpoints

### Health Check
```bash
GET /api/health
```
Returns server and model status.

### Get Features
```bash
GET /api/features
```
Returns list of all features with metadata.

### Make Prediction
```bash
POST /api/predict
Content-Type: application/json

{
  "ra": 112.357708,
  "dec": -12.69596,
  "st_pmra": -5.964,
  ...
}
```
Returns prediction results with confidence scores.

### Get Example Data
```bash
GET /api/example
```
Returns a random example from the dataset.

## 📊 Input Features (40 total)

### Position
- Right Ascension (RA)
- Declination (Dec)

### Stellar Motion
- Proper motion in RA and Dec
- Error measurements

### Transit Properties
- Transit midpoint
- Transit duration
- Transit depth
- Orbital period

### Planet Properties
- Planet radius
- Equilibrium temperature
- Insolation flux

### Stellar Properties
- Effective temperature
- Surface gravity
- Stellar radius
- Distance
- TESS magnitude

## 📈 Model Performance

- **Algorithm**: XGBoost
- **AUC Score**: 0.9534 (95.34%)
- **Training Data**: 1,782 TESS observations
- **Features**: 40 astronomical measurements

## 🎨 Interface Features

- **Dark Space Theme**: Beautiful gradient background
- **Responsive Design**: Works on desktop and mobile
- **Real-time Validation**: Input validation and error handling
- **Visual Feedback**: Loading states and animations
- **Confidence Visualization**: Progress bar and probability display

## 🐛 Troubleshooting

### Port Already in Use
If port 5000 is busy, change it in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Models Not Found
Ensure the `models/` directory contains:
- `xgb_model.pkl`
- `scaler.pkl`
- `feature_names.pkl`

### Import Errors
Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

## 📝 Example Usage

### Using the Web Interface
1. Click "Load Example" button
2. Review the populated values
3. Click "Detect Exoplanet"
4. View results with confidence score

### Using the API with Python
```python
import requests

data = {
    "ra": 112.357708,
    "dec": -12.69596,
    # ... all 40 features
}

response = requests.post('http://localhost:5000/api/predict', json=data)
result = response.json()

print(f"Is Exoplanet: {result['is_exoplanet']}")
print(f"Confidence: {result['confidence']*100:.1f}%")
```

### Using cURL
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d @example_data.json
```

## 🌟 Credits

- **NASA TESS Mission**: Transiting Exoplanet Survey Satellite
- **Model**: XGBoost with 95.34% AUC
- **Data**: TESS exoplanet observations
- **UI Design**: Modern dark space theme

## 📄 License

Built for NASA Hackathon 2025

---

**Enjoy detecting exoplanets! 🌟🪐**
