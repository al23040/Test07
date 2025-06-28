from flask import Flask
from backend.c3.api import register_c3_api  # モジュールパスは適宜修正

def create_app():
    app = Flask(__name__)
    register_c3_api(app)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)