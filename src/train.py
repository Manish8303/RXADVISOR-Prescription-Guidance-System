import joblib
from pathlib import Path
import sys
import os # Added for path manipulation

# ----------------------------------------------------
# FIX: Add the current directory (src) to the Python path 
# to allow direct importing of sibling modules (processing)
# ----------------------------------------------------
sys.path.append(os.path.dirname(__file__))

# Now, we can import without the package dot ('.') notation
# We assume processing is available in the path
from .processing import load_data, preprocess_data, split_data # USE THIS LINE

# We do NOT import recommend here to avoid the circular dependency!
# ----------------------------------------------------


from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report 


# --- Define Paths using Pathlib for robustness ---
BASE_DIR = Path(__file__).resolve().parent.parent

# Define file paths relative to the base directory
DATA_PATH = BASE_DIR / 'data' / 'symptom_to_disease.csv' 
MODEL_DIR = BASE_DIR / 'src' / 'models'
MODEL_PATH = MODEL_DIR / 'disease_recommender_model.joblib' 
ENCODER_PATH = MODEL_DIR / 'disease_label_encoder.joblib' 
FEATURES_PATH = MODEL_DIR / 'symptom_feature_names.joblib' 

def train_model():
    """
    Loads data, preprocesses, splits, trains the model (Random Forest), and saves all necessary files.
    """
    print("--- Starting Professional Model Training Pipeline ---")
    
    # Ensure the models directory exists before saving
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. Load and Preprocess Data
    df = load_data(str(DATA_PATH)) 
    if df is None:
        return

    # X, y_encoded, label_encoder, feature_names from processing.py
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