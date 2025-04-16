from flask import Flask
from app.controller.auth_controller import auth_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = 'supersecretkey' 

    app.register_blueprint(auth_bp)

    return app
