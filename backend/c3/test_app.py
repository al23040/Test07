from flask import Flask
from api import register_c3_api

def create_app():
    app = Flask(__name__)
    register_c3_api(app)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)