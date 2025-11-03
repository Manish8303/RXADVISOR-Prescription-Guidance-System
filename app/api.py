from flask import Flask, request, jsonify
from flask_cors import CORS 
import sys
import os
import json

# =================================================================
# FIX: Explicitly add the 'src' directory to the Python path.
# This tells Pylance/VS Code exactly where to look for 'recommend'.
# =================================================================
# Get the directory of the current file (app) and go up one level (project root)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Add the 'src' folder to the system path
sys.path.append(os.path.join(PROJECT_ROOT, 'src'))

# Import the core recommendation function from the src directory
# Now we can import the module name directly
from recommend import get_recommendation 
# =================================================================

app = Flask(__name__)
# Enable CORS for local testing
CORS(app) 

@app.route('/recommend', methods=['POST'])
def recommend_drug():
    """
    API endpoint to receive patient symptom data and return a drug recommendation.
    """
    try:
        # Get data from the POST request
        data = request.get_json(force=True)
        
        # Get the recommendation result from the ML backend
        result = get_recommendation(data)

        # Return the recommendation as a JSON response
        return jsonify(result)
        
    except Exception as e:
        # Log the error on the server side
        app.logger.error(f"Error during recommendation: {e}")
        # Return a generic error to the client
        return jsonify({"error": "Invalid input or internal processing error.", "details": str(e)}), 400


@app.route('/')
def status():
    return "Medicine Recommendation API is running!"

if __name__ == '__main__':
    # Running on port 5001 to avoid common conflicts
    app.run(host='0.0.0.0', port=5001, debug=True)