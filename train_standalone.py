import pandas as pd
import joblib
from pathlib import Path
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report 


# --- A. Data and Path Definitions ---

# Get the base directory of the entire project (where this script is running)
BASE_DIR = Path(__file__).resolve().parent

# Define file paths relative to the base directory
DATA_PATH = BASE_DIR / 'data' / 'symptom_to_disease.csv' 
MODEL_DIR = BASE_DIR / 'src' / 'models'
MODEL_PATH = MODEL_DIR / 'disease_recommender_model.joblib'
ENCODER_PATH = MODEL_DIR / 'disease_label_encoder.joblib'
FEATURES_PATH = MODEL_DIR / 'symptom_feature_names.joblib' 


# --- B. Integrated Data Processing Functions (from src/processing.py) ---

def load_data(file_path):
    """Loads the dataset."""
    try:
        data = pd.read_csv(file_path)
        print(f"Data loaded successfully from {file_path}. Shape: {data.shape}")
        return data
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None

def preprocess_data(df):
    """Splits features (X) and target (y) for the symptom-to-disease mapping."""
    if df is None:
        return None, None, None, None
    
    # The last column ('Disease') is the target
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    
    # Encode Target Variable (Label Encoding for Multi-Class Classification)
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    feature_names = list(X.columns)
    
    print(f"\nFeature columns (Symptoms): {len(feature_names)} columns found.")
    print(f"Number of unique diseases: {len(le.classes_)}")
    
    return X, y_encoded, le, feature_names

def split_data(X, y, test_size=0.2, random_state=42):
    """Splits the data into training and testing sets."""
    try:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        print(f"\nData split into Train ({len(X_train)}) and Test ({len(X_test)}) sets (Stratified).")
    except ValueError as e:
        print(f"\nWarning: Stratified split failed ({e}). Splitting without stratification.")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        print(f"Data split into Train ({len(X_train)}) and Test ({len(X_test)}) sets (Non-Stratified).")
        
    return X_train, X_test, y_train, y_test


# --- C. Training and Saving Logic (from src/train.py) ---

def train_model():
    """
    Loads data, preprocesses, splits, trains the model (Random Forest), and saves all necessary files.
    """
    print("--- Starting FINAL Standalone Training Pipeline ---")
    
    # Ensure the models directory exists before saving
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. Load and Preprocess Data
    df = load_data(str(DATA_PATH)) 
    if df is None:
        return

    X, y_encoded, label_encoder, feature_names = preprocess_data(df)
    
    if X is None or len(X) < 2:
        print("Error: Insufficient data after preprocessing.")
        return

    # 2. Split Data
    try:
        X_train, X_test, y_train, y_test = split_data(X, y_encoded)
    except Exception as e:
        print(f"Error during data splitting: {e}. Aborting training.")
        return
    
    # 3. Initialize and Train Model
    print("\nTraining Random Forest Classifier (Disease Prediction)...")
    model = RandomForestClassifier(n_estimators=100, random_state=42) 
    model.fit(X_train, y_train)
    print("Model training complete.")
    
    # 4. Evaluate Model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\nModel Accuracy on Test Set: {accuracy:.4f}")
    print("\nClassification Report:")
    
    # FIX: Use labels=model.classes_ to include only classes present in the test set
    print(classification_report(y_test, y_pred, target_names=label_encoder.classes_, labels=model.classes_))
    
    # 5. Save Model Artifacts
    print("\nSaving model artifacts...")
    
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to: {MODEL_PATH}")
    
    joblib.dump(label_encoder, ENCODER_PATH)
    print(f"Disease Label Encoder saved to: {ENCODER_PATH}")
    
    joblib.dump(feature_names, FEATURES_PATH)
    print(f"Symptom feature names saved to: {FEATURES_PATH}")
    
    print("\n--- Training Pipeline Complete ---")

if __name__ == '__main__':
    train_model()