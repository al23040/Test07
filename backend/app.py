from flask import Flask, request, jsonify
from flask_cors import CORS
from c3 import register_c3_api
from c4 import register_c4_api
from c5 import register_c5_api, AccountManager


app = Flask(__name__)
CORS(app)

# Initialize C5 Account Manager
account_manager = AccountManager()

# Register API endpoints
c4_api = register_c4_api(app)  # C4 Condition Processing
c5_api = register_c5_api(app)  # C5 Account Management

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'component': 'Course Registration Support System'}), 200

@app.route('/api/users/login', methods=['POST'])
def user_login():
    """User login endpoint"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        password = data.get('password')

        if not user_id or not password:
            return jsonify({'error': 'Missing user_id or password'}), 400

        # Validate user credentials
        is_valid = account_manager.authenticate_user(user_id, password)

        if is_valid:
            return jsonify({'status': 'success', 'message': 'Login successful'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/users/register', methods=['POST'])
def user_register():
    """User registration endpoint"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        password = data.get('password')

        if not user_id or not password:
            return jsonify({'error': 'Missing user_id or password'}), 400

        # Add user to database
        success = account_manager.create_user_account(user_id, password)
        if not success:
            return jsonify({'status': 'error', 'message': 'Failed to create user account'}), 400

        return jsonify({'status': 'success', 'message': 'User registered successfully'}), 201

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
