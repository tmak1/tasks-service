import os
from flask import Flask, jsonify
from flask_cors import CORS
from database import init_db, db_name
from tasks_routes import tasks_bp

app = Flask(__name__)

port = int(os.environ.get('PORT', 4000))
frontend_service_host = int(os.environ.get('PORT', 5000))
frontend_service_port = int(os.environ.get('PORT', 5000))

CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

app.register_blueprint(tasks_bp)

if __name__ == '__main__':
    try:
        init_db()
    except Exception as e:
        print(f'{db_name} not ready yet: {e}')
    
    app.run(host='0.0.0.0', port=port)