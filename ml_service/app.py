from flask import Flask, request, jsonify
import pickle
import os

app = Flask(__name__)

# Determine paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, 'model')

# Global variables for models
vectorizer = None
url_model = None
type_model = None

def load_models():
    global vectorizer, url_model, type_model
    try:
        with open(os.path.join(MODEL_DIR, 'vectorizer.pkl'), 'rb') as f:
            vectorizer = pickle.load(f)
        with open(os.path.join(MODEL_DIR, 'url_model.pkl'), 'rb') as f:
            url_model = pickle.load(f)
        with open(os.path.join(MODEL_DIR, 'type_model.pkl'), 'rb') as f:
            type_model = pickle.load(f)
        return True
    except FileNotFoundError:
        print("Models not found. Please run train_model.py first.")
        return False

@app.before_request
def check_models():
    if vectorizer is None or url_model is None or type_model is None:
        load_models()

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({'error': 'No URL provided'}), 400
        
        url = data['url']
        
        # Check if models are loaded
        if vectorizer is None:
            return jsonify({'error': 'ML models are not loaded. Run train_model.py first.'}), 500

        # Feature extraction
        X = vectorizer.transform([url])
        
        # Predict label
        prediction = url_model.predict(X)[0]
        
        # Determine attack type
        if prediction == 'Malicious':
            attack_type = type_model.predict(X)[0]
        else:
            attack_type = 'None'
            
        # Determine risk level
        if prediction == 'Safe':
            risk_level = 'Low'
            attack_type = 'None' # Force safety
        else:
            if attack_type in ['SQL Injection', 'Command Injection', 'Path Traversal']:
                risk_level = 'High'
            elif attack_type == 'XSS':
                risk_level = 'Medium'
            else:
                risk_level = 'Low'

        return jsonify({
            'url': url,
            'prediction': prediction,
            'attack_type': attack_type,
            'risk_level': risk_level
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'running'})

if __name__ == '__main__':
    # Load models before running
    load_models()
    # Run the Flask app
    print("Starting ML API Service on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=False)
