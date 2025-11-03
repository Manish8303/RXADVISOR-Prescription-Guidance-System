import joblib
import pandas as pd
from pathlib import Path
import numpy as np
import json

# --- Define Paths ---
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / 'src' / 'models'
DATA_DIR = BASE_DIR / 'data' 

# Model Artifacts
MODEL_PATH = MODEL_DIR / 'disease_recommender_model.joblib'
ENCODER_PATH = MODEL_DIR / 'disease_label_encoder.joblib'
FEATURES_PATH = MODEL_DIR / 'symptom_feature_names.joblib'

# Real-World Mapping Data
DRUG_MAPPING_PATH = DATA_DIR / 'drug_mapping.json'

# --- Global Artifacts (Loaded once) ---
MODEL = None
LABEL_ENCODER = None
FEATURE_NAMES = None
DRUG_MAPPING = {} 

def load_artifacts():
    """Loads the trained model, label encoder, feature names, and drug mapping."""
    global MODEL, LABEL_ENCODER, FEATURE_NAMES, DRUG_MAPPING
    
    print("Loading model artifacts...")
    try:
        # Load the artifacts created by train.py
        MODEL = joblib.load(MODEL_PATH)
        LABEL_ENCODER = joblib.load(ENCODER_PATH)
        FEATURE_NAMES = joblib.load(FEATURES_PATH)
        
        # Load the real-world drug mapping
        with open(DRUG_MAPPING_PATH, 'r') as f:
            DRUG_MAPPING = json.load(f)
            
        print("Model and Drug Mapping artifacts loaded successfully.")
    except FileNotFoundError as e:
        print(f"Error loading required files: {e}")
        print("Ensure you have run 'python3 -m src.train' successfully and created 'data/drug_mapping.json'.")
        raise # Re-raise the error so the API knows it can't start

def create_input_features(user_data):
    """
    Converts raw user input (symptom dictionary) into the feature vector 
    expected by the trained model.
    """
    # Load artifacts if they haven't been loaded yet (needed if called outside of API/main)
    if FEATURE_NAMES is None:
        load_artifacts() 
    
    # Create an empty DataFrame with all expected symptom columns set to 0
    input_vector = pd.DataFrame(0, index=[0], columns=FEATURE_NAMES)
    
    # Fill in the presence (1) for symptoms reported by the user
    for symptom, presence in user_data.items():
        if symptom in FEATURE_NAMES and (presence == 1 or presence == '1' or presence is True):
             input_vector[symptom] = 1
            
    return input_vector

def get_recommendation(user_data):
    """Generates a disease prediction and drug recommendation based on user input."""
    
    # 1. Ensure Model is Loaded
    if MODEL is None:
        try:
            load_artifacts()
        except Exception:
            return {"error": "Model artifacts not found. Please train the model first."}

    # 2. Prepare Input Data
    try:
        input_vector = create_input_features(user_data)
    except Exception as e:
        return {"error": f"Error preparing input: {e}"}

    # 3. Make Prediction
    prediction_encoded = MODEL.predict(input_vector)[0]
    
    # 4. Inverse Transform to get Disease Name
    predicted_disease = LABEL_ENCODER.inverse_transform([prediction_encoded])[0]
    
    # 5. Get Recommendation Details from Mapping
    recommendation_details = DRUG_MAPPING.get(
        predicted_disease, 
        {"drug": "General consultation recommended.", "notes": "No specific drug mapping found for this condition. Consult a physician."}
    )

    # 6. Get Prediction Probability (Confidence)
    probabilities = MODEL.predict_proba(input_vector)[0]
    confidence = np.max(probabilities) * 100 
    
    # 7. Compile Final Result
    return {
        "predicted_disease": predicted_disease,
        "recommended_drug": recommendation_details['drug'],
        "confidence": f"{confidence:.2f}%",
        "notes": recommendation_details['notes']
    }


if __name__ == '__main__':
    # Test case: Common Cold symptoms
    # Load artifacts only when running this file directly
    load_artifacts() 
    
    partial_input = {'cough': 1, 'high_fever': 1, 'headache': 1}
    
    recommendation = get_recommendation(partial_input)
    print("\n--- Testing Professional Recommendation System ---")
    print("Input Symptoms:", {k:v for k,v in partial_input.items() if v==1})
    
    print("\nRecommendation Result:")
    for k, v in recommendation.items():
        print(f"  {k.replace('_', ' ').title():<20}: {v}")