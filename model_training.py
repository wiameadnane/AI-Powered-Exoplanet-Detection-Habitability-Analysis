"""
Model Training Module for Exoplanet Detection
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score
import xgboost as xgb
import joblib
import os

def train_model(df):
    """
    Train XGBoost model on provided data
    Returns performance metrics and saves model files
    """
    print("Starting model training...")
    
    # Prepare data
    y = df['tfopwg_disp']
    X = df.drop(columns=['tfopwg_disp'])
    
    # Apply normalization
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_scaled = pd.DataFrame(X_scaled, columns=X.columns, index=X.index)
    
    # Split data: 60% train, 20% validation, 20% test
    X_train, X_temp, y_train, y_temp = train_test_split(
        X_scaled, y, test_size=0.4, random_state=42, stratify=y
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp
    )
    
    # XGBoost parameters
    xgb_params = {
        'objective': 'binary:logistic',
        'eval_metric': 'logloss',
        'max_depth': 6,
        'learning_rate': 0.1,
        'n_estimators': 100,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'random_state': 42
    }
    
    # Train model
    xgb_model = xgb.XGBClassifier(**xgb_params)
    try:
        # First try with early_stopping_rounds as a parameter to fit()
        xgb_model.fit(X_train, y_train,
                     eval_set=[(X_val, y_val)],
                     early_stopping_rounds=10,
                     verbose=False)
    except TypeError:
        # If that fails, try with early_stopping as a model parameter
        xgb_params['early_stopping_rounds'] = 10
        xgb_model = xgb.XGBClassifier(**xgb_params)
        xgb_model.fit(X_train, y_train,
                     eval_set=[(X_val, y_val)],
                     verbose=False)
    
    # Calculate metrics
    y_test_proba = xgb_model.predict_proba(X_test)[:, 1]
    test_auc = roc_auc_score(y_test, y_test_proba)
    
    # Calculate feature importance
    feature_importance = pd.DataFrame({
        'feature': X_scaled.columns,
        'importance': xgb_model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    # Save models and preprocessing objects
    os.makedirs('models', exist_ok=True)
    joblib.dump(xgb_model, 'models/xgb_model.pkl')
    joblib.dump(scaler, 'models/scaler.pkl')
    joblib.dump(list(X_scaled.columns), 'models/feature_names.pkl')
    
    # Prepare results
    results = {
        'auc_score': float(test_auc),
        'dataset_size': len(df),
        'training_size': len(X_train),
        'validation_size': len(X_val),
        'test_size': len(X_test),
        'exoplanet_ratio': float(y.mean()),
        'top_features': feature_importance.head(10).to_dict('records'),
        'training_date': pd.Timestamp.now().isoformat()
    }
    
    return results
