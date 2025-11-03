from flask import Flask, request, jsonify
import sys
import os
import json

# Add the src directory to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import the core recommendation function from the src directory
from src.recommend import get_recommendation 

app = Flask(__name__)

@app.route('/recommend', methods=['POST'])
def recommend_drug():
    """
    API endpoint to receive patient data and return a drug recommendation.
    """
    try:
        # Get data from the POST request
        data = request.get_json(force=True)
        
        # NOTE: The ML model only uses symptom data (0 or 1), 
        # but the API still receives the full JSON from the UI.
        
        # Get the recommendation result
        result = get_recommendation(data)

        # Return the recommendation as a JSON response
        return jsonify(result)
        
    except Exception as e:
        app.logger.error(f"Error during recommendation: {e}")
        return jsonify({"error": "Invalid input or internal processing error.", "details": str(e)}), 400


@app.route('/')
def status():
    return "Medicine Recommendation API is running!"

if __name__ == '__main__':
    # Running on port 5001 to avoid common conflicts
    app.run(host='0.0.0.0', port=5001, debug=True)