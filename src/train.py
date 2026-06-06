import os
import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRegressor

def train_and_evaluate():
    """
    Loads dataset, splits it into train/test sets, scales features,
    trains Random Forest and XGBoost models, evaluates them,
    and serializes the best performing model + scaler.
    """
    # 1. Load data
    input_path = 'data/housing_data.csv'
    if not os.path.exists(input_path):
        print(f"Error: Dataset {input_path} not found. Please run generate_data.py first.")
        return
        
    df = pd.read_csv(input_path)
    
    # 2. Separate Features and Target
    feature_cols = ['TotalSqFt', 'Bedrooms', 'Bathrooms', 'OverallQuality', 'YearBuilt', 'RoadWidth', 'RoadType_RCC']
    target_col = 'Price'
    
    X = df[feature_cols]
    y = df[target_col]
    
    # 3. Train-Test Split (80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # 4. Standard Scaling
    # Save the scaler so we can scale new inputs in the web UI identically
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Create models directory
    models_dir = 'models'
    os.makedirs(models_dir, exist_ok=True)
    
    # Save the scaler
    scaler_path = os.path.join(models_dir, 'scaler.pkl')
    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)
    print(f"Saved scaler to {scaler_path}")
    
    # 5. Train Random Forest Regressor
    rf_model = RandomForestRegressor(
        n_estimators=100, 
        max_depth=10, 
        random_state=42,
        n_jobs=-1
    )
    rf_model.fit(X_train_scaled, y_train)
    
    # Evaluate Random Forest
    rf_preds = rf_model.predict(X_test_scaled)
    rf_rmse = np.sqrt(mean_squared_error(y_test, rf_preds))
    rf_r2 = r2_score(y_test, rf_preds)
    
    print("\n" + "="*40)
    print("Random Forest Regressor Results")
    print("="*40)
    print(f"Test RMSE: ${rf_rmse:,.2f}")
    print(f"Test R2 Score: {rf_r2:.4f}")
    
    # 6. Train XGBoost Regressor
    xgb_model = XGBRegressor(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.08,
        random_state=42,
        n_jobs=-1
    )
    xgb_model.fit(X_train_scaled, y_train)
    
    # Evaluate XGBoost
    xgb_preds = xgb_model.predict(X_test_scaled)
    xgb_rmse = np.sqrt(mean_squared_error(y_test, xgb_preds))
    xgb_r2 = r2_score(y_test, xgb_preds)
    
    print("\n" + "="*40)
    print("XGBoost Regressor Results")
    print("="*40)
    print(f"Test RMSE: ${xgb_rmse:,.2f}")
    print(f"Test R2 Score: {xgb_r2:.4f}")
    print("="*40 + "\n")
    
    # 7. Identify the Best Model
    # Compare R2 scores
    if xgb_r2 > rf_r2:
        best_model = xgb_model
        best_name = "XGBoost"
        best_rmse = xgb_rmse
        best_r2 = xgb_r2
    else:
        best_model = rf_model
        best_name = "Random Forest"
        best_rmse = rf_rmse
        best_r2 = rf_r2
        
    print(f"Champion Model Selected: {best_name} with R2 Score of {best_r2:.4f}")
    
    # Save the Champion Model
    model_path = os.path.join(models_dir, 'best_model.pkl')
    
    # Package the model, the metadata (model name, test metrics) into a dict
    model_payload = {
        'model': best_model,
        'model_name': best_name,
        'rmse': best_rmse,
        'r2': best_r2,
        'feature_names': feature_cols
    }
    
    with open(model_path, 'wb') as f:
        pickle.dump(model_payload, f)
        
    print(f"Successfully saved champion model payload to {model_path}")

if __name__ == '__main__':
    train_and_evaluate()
