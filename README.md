# LifeBeyond 🌍 The NASA International Space Apps Challenge (UM6P & NASA)

**AI-Powered Exoplanet Detection & Habitability Analysis**

LifeBeyond is an advanced machine learning system that detects exoplanets from NASA TESS mission data and analyzes their potential habitability using state-of-the-art AI models.

<p align="center">
  <img src="static/lifebeyond-logo.png" alt="LifeBeyond Logo" width="300">
</p>

## 🌟 Features

- **Exoplanet Detection**: XGBoost-based machine learning model trained on NASA TESS data
- **Habitability Analysis**: GPT-5 powered Earth similarity scoring and analysis
- **Visual Generation**: AI-generated artistic visualizations of detected exoplanets
- **Data Management**: PostgreSQL database for storing and managing observations
- **Model Retraining**: Upload new data and retrain the model with updated observations
- **Clean UI**: Modern, minimal interface for scientific data analysis

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL database
- OpenRouter API key (for habitability analysis)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/lifebeyond.git
   cd lifebeyond
   ```

2. **Install dependencies**
   ```bash
   # On Windows
   install_requirements.bat
   
   # On Linux/Mac
   chmod +x install_requirements.sh
   ./install_requirements.sh
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   OPENROUTER_API_KEY=your_api_key_here
   DATABASE_URL=postgresql://user:password@localhost:5432/dbname
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   
   Navigate to `http://127.0.0.1:5000`

## 📊 Project Structure

```
lifebeyond/
├── app.py                 # Main Flask application
├── db.py                  # Database management
├── model_training.py      # Model training logic
├── image_gen.py          # Exoplanet visualization generator
├── models/               # Trained ML models
│   ├── xgb_model.pkl
│   ├── scaler.pkl
│   └── feature_names.pkl
├── templates/            # HTML templates
│   └── index.html
├── static/               # Static assets
│   ├── lifebeyond-logo.png
│   └── generated/        # Generated images (ignored by git)
├── requirements.txt      # Python dependencies
└── .env                  # Environment variables (not in repo)
```

## 🔬 How It Works

### 1. Exoplanet Detection
- Uses XGBoost classifier trained on 40 features from NASA TESS observations
- Features include orbital period, planet radius, stellar properties, and transit characteristics
- Achieves high accuracy with AUC score tracking

### 2. Habitability Analysis
- Powered by GPT-5 via OpenRouter API
- Compares detected exoplanets to Earth's characteristics
- Provides Earth similarity score and detailed analysis
- Considers temperature, radiation, size, and composition

### 3. Visualization
- Generates artistic representations using Pollinations.ai
- Based on actual exoplanet parameters
- Cached for performance

## 🛠️ API Endpoints

- `GET /` - Main application interface
- `POST /api/predict` - Detect exoplanet from observation data
- `POST /api/habitability` - Analyze habitability of detected exoplanet
- `GET /api/features` - Get list of required features
- `GET /api/example` - Load example TESS observation
- `POST /api/upload-csv` - Upload additional training data
- `POST /api/export-dataset` - Export current dataset
- `POST /api/retrain` - Retrain model with new data
- `GET /api/health` - Check database connection

## 📈 Model Performance

The XGBoost model is trained on NASA TESS mission data with:
- 60% training set
- 20% validation set
- 20% test set
- Feature importance tracking
- Regular retraining capability

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- NASA TESS Mission for providing exoplanet observation data
- OpenRouter for GPT-5 API access
- Pollinations.ai for image generation
- The open-source community


**Built with ❤️ for space exploration and the search for life beyond Earth**
