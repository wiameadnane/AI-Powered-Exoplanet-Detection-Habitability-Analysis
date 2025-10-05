"""
Exoplanet Detection Web Application
Flask Backend API
"""

from flask import Flask, request, jsonify, render_template, send_file
import joblib
import numpy as np
import pandas as pd
import os
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from db import DatabaseManager
from model_training import train_model
from image_gen import generate_exoplanet_image

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for all routes

# Create static folder for generated images
os.makedirs('static/generated', exist_ok=True)

# File upload configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize OpenAI client for habitability analysis
try:
    print("🔄 Initializing LLM client...")
    api_key = os.getenv("OPENROUTER_API_KEY")
    print(f"📝 API Key found: {'Yes' if api_key else 'No'}")
    
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in environment variables")
    
    print("🔄 Creating OpenAI client...")    
    openai_client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )
    
    print("🔄 Testing API connection...")
    try:
        test_completion = openai_client.chat.completions.create(
            model="openai/gpt-5-chat",  # Using GPT-5
            messages=[{"role": "user", "content": "test"}]
        )
        print(f"🔍 API Response: {test_completion}")
    except Exception as api_error:
        print(f"⚠️  API Test Error Details: {str(api_error)}")
        raise
    
    llm_enabled = True
    print("✅ OpenAI client initialized and tested successfully")
    print(f"✅ Test response received: {test_completion.model}")
except Exception as e:
    print(f"⚠️  LLM initialization failed with error: {str(e)}")
    print(f"⚠️  Error type: {type(e).__name__}")
    openai_client = None
    llm_enabled = False

# Load the trained model, scaler, and feature names
MODEL_PATH = 'models/xgb_model.pkl'
SCALER_PATH = 'models/scaler.pkl'
FEATURES_PATH = 'models/feature_names.pkl'

print("Loading models...")
try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    feature_names = joblib.load(FEATURES_PATH)
    print("✅ Models loaded successfully!")
    print(f"✅ Features: {len(feature_names)} features loaded")
except Exception as e:
    print(f"❌ Error loading models: {e}")
    model = None
    scaler = None
    feature_names = None

# Feature metadata for better UI
FEATURE_METADATA = {
    'ra': {'label': 'Right Ascension (deg)', 'group': 'Position'},
    'dec': {'label': 'Declination (deg)', 'group': 'Position'},
    'st_pmra': {'label': 'Proper Motion RA (mas/yr)', 'group': 'Stellar Motion'},
    'st_pmraerr1': {'label': 'PM RA Error +', 'group': 'Stellar Motion'},
    'st_pmraerr2': {'label': 'PM RA Error -', 'group': 'Stellar Motion'},
    'st_pmdec': {'label': 'Proper Motion Dec (mas/yr)', 'group': 'Stellar Motion'},
    'st_pmdecerr1': {'label': 'PM Dec Error +', 'group': 'Stellar Motion'},
    'st_pmdecerr2': {'label': 'PM Dec Error -', 'group': 'Stellar Motion'},
    'pl_tranmid': {'label': 'Transit Midpoint (BJD)', 'group': 'Transit Properties'},
    'pl_tranmiderr1': {'label': 'Transit Mid Error +', 'group': 'Transit Properties'},
    'pl_tranmiderr2': {'label': 'Transit Mid Error -', 'group': 'Transit Properties'},
    'pl_orbper': {'label': 'Orbital Period (days)', 'group': 'Orbital Properties'},
    'pl_orbpererr1': {'label': 'Orbital Period Error +', 'group': 'Orbital Properties'},
    'pl_orbpererr2': {'label': 'Orbital Period Error -', 'group': 'Orbital Properties'},
    'pl_trandurh': {'label': 'Transit Duration (hours)', 'group': 'Transit Properties'},
    'pl_trandurherr1': {'label': 'Transit Duration Error +', 'group': 'Transit Properties'},
    'pl_trandurherr2': {'label': 'Transit Duration Error -', 'group': 'Transit Properties'},
    'pl_trandep': {'label': 'Transit Depth (ppm)', 'group': 'Transit Properties'},
    'pl_trandeperr1': {'label': 'Transit Depth Error +', 'group': 'Transit Properties'},
    'pl_trandeperr2': {'label': 'Transit Depth Error -', 'group': 'Transit Properties'},
    'pl_rade': {'label': 'Planet Radius (Earth radii)', 'group': 'Planet Properties'},
    'pl_radeerr1': {'label': 'Planet Radius Error +', 'group': 'Planet Properties'},
    'pl_radeerr2': {'label': 'Planet Radius Error -', 'group': 'Planet Properties'},
    'pl_insol': {'label': 'Insolation Flux (Earth flux)', 'group': 'Planet Properties'},
    'pl_eqt': {'label': 'Equilibrium Temperature (K)', 'group': 'Planet Properties'},
    'st_tmag': {'label': 'TESS Magnitude', 'group': 'Stellar Properties'},
    'st_tmagerr1': {'label': 'TESS Mag Error +', 'group': 'Stellar Properties'},
    'st_tmagerr2': {'label': 'TESS Mag Error -', 'group': 'Stellar Properties'},
    'st_dist': {'label': 'Distance (pc)', 'group': 'Stellar Properties'},
    'st_disterr1': {'label': 'Distance Error +', 'group': 'Stellar Properties'},
    'st_disterr2': {'label': 'Distance Error -', 'group': 'Stellar Properties'},
    'st_teff': {'label': 'Effective Temperature (K)', 'group': 'Stellar Properties'},
    'st_tefferr1': {'label': 'Eff. Temp Error +', 'group': 'Stellar Properties'},
    'st_tefferr2': {'label': 'Eff. Temp Error -', 'group': 'Stellar Properties'},
    'st_logg': {'label': 'Surface Gravity (log g)', 'group': 'Stellar Properties'},
    'st_loggerr1': {'label': 'Surface Gravity Error +', 'group': 'Stellar Properties'},
    'st_loggerr2': {'label': 'Surface Gravity Error -', 'group': 'Stellar Properties'},
    'st_rad': {'label': 'Stellar Radius (Solar radii)', 'group': 'Stellar Properties'},
    'st_raderr1': {'label': 'Stellar Radius Error +', 'group': 'Stellar Properties'},
    'st_raderr2': {'label': 'Stellar Radius Error -', 'group': 'Stellar Properties'},
}

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/features', methods=['GET'])
def get_features():
    """Return the list of features and their metadata"""
    if feature_names is None:
        return jsonify({'error': 'Features not loaded'}), 500
    
    features_with_metadata = []
    for feature in feature_names:
        metadata = FEATURE_METADATA.get(feature, {'label': feature, 'group': 'Other'})
        features_with_metadata.append({
            'name': feature,
            'label': metadata['label'],
            'group': metadata['group']
        })
    
    return jsonify({'features': features_with_metadata})

@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Predict exoplanet detection
    Expects JSON with feature values
    """
    try:
        if model is None or scaler is None or feature_names is None:
            return jsonify({'error': 'Models not loaded properly'}), 500
        
        # Get data from request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract features in correct order
        features = []
        missing_features = []
        
        for feature_name in feature_names:
            if feature_name in data:
                try:
                    features.append(float(data[feature_name]))
                except (ValueError, TypeError):
                    return jsonify({'error': f'Invalid value for {feature_name}'}), 400
            else:
                missing_features.append(feature_name)
        
        if missing_features:
            return jsonify({'error': f'Missing features: {", ".join(missing_features)}'}), 400
        
        # Convert to numpy array and reshape
        X = np.array(features).reshape(1, -1)
        
        # Apply scaling
        X_scaled = scaler.transform(X)
        
        # Make prediction
        prediction = model.predict(X_scaled)[0]
        prediction_proba = model.predict_proba(X_scaled)[0]
        
        # Prepare response
        result = {
            'prediction': int(prediction),
            'is_exoplanet': bool(prediction == 1),
            'confidence': float(prediction_proba[1]),
            'probabilities': {
                'not_exoplanet': float(prediction_proba[0]),
                'exoplanet': float(prediction_proba[1])
            },
            'label': 'Exoplanet Detected! 🌟' if prediction == 1 else 'Not an Exoplanet ❌'
        }
        
        # If it's an exoplanet, analyze habitability and generate visualization
        if prediction == 1:
            print("🌍 Analyzing habitability...")
            if llm_enabled and openai_client is not None:
                habitability_result = analyze_habitability(data)
                result['habitability'] = habitability_result
            else:
                print("⚠️ LLM not enabled or client not available")
                result['habitability'] = {
                    'error': 'LLM not available',
                    'habitability_score': None,
                    'explanation': 'Habitability analysis requires OpenAI API key',
                    'success': False
                }
            
            # Generate visualization regardless of LLM status
            print("🎨 Generating exoplanet visualization...")
            visualization_result = generate_exoplanet_image(data)
            result['visualization'] = visualization_result
        else:
            result['habitability'] = None
            result['visualization'] = None
            
        print(f"Prediction result: {result}")
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/example', methods=['GET'])
def get_example():
    """Return an example from the dataset"""
    try:
        df = pd.read_csv('cleaned_data.csv')
        
        # Get a random row (excluding the target column)
        row = df.sample(n=1).iloc[0]
        
        example_data = {}
        for feature in feature_names:
            if feature in row.index:
                example_data[feature] = float(row[feature])
        
        # Also return the actual label
        actual_label = int(row['tfopwg_disp']) if 'tfopwg_disp' in row.index else None
        
        return jsonify({
            'features': example_data,
            'actual_label': actual_label
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'scaler_loaded': scaler is not None,
        'features_loaded': feature_names is not None,
        'num_features': len(feature_names) if feature_names is not None else 0,
        'llm_enabled': llm_enabled
    })

def analyze_habitability(exoplanet_data):
    """
    Analyze exoplanet habitability using LLM
    Returns habitability percentage and explanation
    """
    if not llm_enabled or openai_client is None:
        return {
            'error': 'LLM not available',
            'habitability_score': None,
            'explanation': 'Habitability analysis requires OpenAI API key'
        }
    
    try:
        # Extract relevant features
        pl_orbper = exoplanet_data.get('pl_orbper', 'N/A')
        pl_rade = exoplanet_data.get('pl_rade', 'N/A')
        pl_insol = exoplanet_data.get('pl_insol', 'N/A')
        pl_eqt = exoplanet_data.get('pl_eqt', 'N/A')
        st_teff = exoplanet_data.get('st_teff', 'N/A')
        st_rad = exoplanet_data.get('st_rad', 'N/A')
        st_logg = exoplanet_data.get('st_logg', 'N/A')
        
        prompt = f"""You are an exoplanet scientist analyzing Earth similarity. Compare this exoplanet to Earth.

EARTH REFERENCE:
• Orbital Period: 365.256 days
• Planet Radius: 1.0 R⊕
• Insolation Flux: 1.0 Earth flux
• Equilibrium Temperature: 255 K
• Star Temperature: 5772 K

EXOPLANET DATA:
• Orbital Period: {pl_orbper} days
• Planet Radius: {pl_rade} R⊕
• Insolation Flux: {pl_insol} Earth flux
• Equilibrium Temperature: {pl_eqt} K
• Star Temperature: {st_teff} K

REQUIRED FORMAT:
Start with: "HABITABILITY SCORE: X%"

Then write 2-3 clear sentences explaining:
- Temperature and liquid water potential
- Planet size and composition
- Radiation environment
- Overall habitability assessment

Use asterisks (*) for emphasis on key points. Be realistic - most exoplanets score below 30%."""

        print("🔄 Starting habitability analysis...")
        try:
            completion = openai_client.chat.completions.create(
                model="openai/gpt-5-chat",  # Using GPT-5 for analysis
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            print("✅ Received habitability analysis response")
            print(f"🔍 Model used: {completion.model}")
        except Exception as analysis_error:
            print(f"⚠️  Habitability Analysis Error: {str(analysis_error)}")
            raise
        
        response_text = completion.choices[0].message.content
        
        # Try to extract percentage from response
        import re
        
        # First try to find "HABITABILITY SCORE: X%" pattern
        score_match = re.search(r'HABITABILITY SCORE:\s*(\d+(?:\.\d+)?)\s*%', response_text, re.IGNORECASE)
        
        if score_match:
            habitability_score = float(score_match.group(1))
            # Remove the score line from explanation
            explanation = re.sub(r'HABITABILITY SCORE:\s*\d+(?:\.\d+)?%\s*', '', response_text, flags=re.IGNORECASE).strip()
        else:
            # Fallback: try to find any percentage in the first line or sentence
            first_line = response_text.split('\n')[0]
            percentage_match = re.search(r'(\d+(?:\.\d+)?)\s*%', first_line)
            if percentage_match:
                habitability_score = float(percentage_match.group(1))
            else:
                # Last resort: find any percentage in the text
                percentage_match = re.search(r'(\d+(?:\.\d+)?)\s*%', response_text)
                habitability_score = float(percentage_match.group(1)) if percentage_match else None
            explanation = response_text
        
        return {
            'habitability_score': habitability_score,
            'explanation': explanation if 'explanation' in locals() else response_text,
            'success': True
        }
        
    except Exception as e:
        return {
            'error': str(e),
            'habitability_score': None,
            'explanation': f'Error analyzing habitability: {str(e)}',
            'success': False
        }

@app.route('/api/habitability', methods=['POST'])
def get_habitability():
    """
    Analyze exoplanet habitability
    Expects JSON with exoplanet feature values
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        if not llm_enabled:
            return jsonify({
                'error': 'LLM not enabled. Please set OPENROUTER_API_KEY in .env file'
            }), 503
        
        result = analyze_habitability(data)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload-csv', methods=['POST'])
def upload_csv():
    """
    Upload CSV file and add data to PostgreSQL database
    """
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only CSV files are allowed'}), 400
        
        # Save the uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Add data to database
        db = DatabaseManager(table_name='tess_dataset')
        result = db.add_csv_to_database(filepath)
        
        if not result.get('success'):
            return jsonify({
                'success': False,
                'error': f"Database error: {result.get('error')}"
            }), 500
        
        rows_inserted = result.get('rows_inserted', 0)
        
        # Get updated row count
        count_result = db.get_row_count()
        total_rows = count_result.get('count', 0) if count_result.get('success') else 0
        
        # Clean up uploaded file
        os.remove(filepath)
        
        return jsonify({
            'success': True,
            'message': f'Successfully added {rows_inserted} rows to database',
            'rows_inserted': rows_inserted,
            'total_rows': total_rows
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/export-dataset', methods=['POST'])
def export_dataset():
    """
    Export entire database to whole_dataset.csv
    """
    try:
        db = DatabaseManager(table_name='tess_dataset')
        
        # Export to CSV
        output_path = 'whole_dataset.csv'
        result = db.export_to_csv(output_path)
        
        if not result.get('success'):
            return jsonify({
                'success': False,
                'error': f"Export error: {result.get('error')}"
            }), 500
        
        return jsonify({
            'success': True,
            'message': f'Successfully exported {result.get("rows_exported")} rows',
            'rows_exported': result.get('rows_exported'),
            'output_path': output_path
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/download-dataset', methods=['GET'])
def download_dataset():
    """
    Download the whole_dataset.csv file
    """
    try:
        filepath = 'whole_dataset.csv'
        if not os.path.exists(filepath):
            return jsonify({'error': 'Dataset not found. Please export first.'}), 404
        
        return send_file(
            filepath,
            mimetype='text/csv',
            as_attachment=True,
            download_name='whole_dataset.csv'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/database-status', methods=['GET'])
def database_status():
    """
    Get database connection status and row count
    """
    try:
        db = DatabaseManager(table_name='tess_dataset')
        count_result = db.get_row_count()
        
        if count_result.get('success'):
            return jsonify({
                'connected': True,
                'row_count': count_result.get('count', 0)
            })
        else:
            return jsonify({
                'connected': False,
                'error': count_result.get('error')
            }), 500
            
    except Exception as e:
        return jsonify({
            'connected': False,
            'error': str(e)
        }), 500

@app.route('/api/retrain', methods=['POST'])
def retrain_model():
    """
    Retrain the model using all data in the database
    Returns new model performance metrics
    """
    try:
        # Get data from database
        db = DatabaseManager(table_name='tess_dataset')
        result = db.export_to_csv('temp_training_data.csv')
        
        if not result.get('success'):
            return jsonify({
                'success': False,
                'error': f"Database export error: {result.get('error')}"
            }), 500
        
        # Load the data
        try:
            df = pd.read_csv('temp_training_data.csv')
            os.remove('temp_training_data.csv')  # Clean up temp file
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f"Error loading data: {str(e)}"
            }), 500
        
        # Check if we have enough data
        if len(df) < 100:  # Minimum threshold for training
            return jsonify({
                'success': False,
                'error': "Not enough data for training. Minimum 100 samples required."
            }), 400
        
        # Train model
        try:
            results = train_model(df)
            
            # Reload the model and scaler
            global model, scaler, feature_names
            model = joblib.load('models/xgb_model.pkl')
            scaler = joblib.load('models/scaler.pkl')
            feature_names = joblib.load('models/feature_names.pkl')
            
            return jsonify({
                'success': True,
                'message': 'Model retrained successfully',
                'metrics': results
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f"Error during training: {str(e)}"
            }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("="*60)
    print("🚀 Exoplanet Detection API")
    print("="*60)
    print(f"Model: {MODEL_PATH}")
    print(f"Scaler: {SCALER_PATH}")
    print(f"Features: {len(feature_names) if feature_names else 0}")
    print("="*60)
    print("Starting server on http://localhost:5000")
    print("="*60)
    app.run(debug=True, host='0.0.0.0', port=5000)
