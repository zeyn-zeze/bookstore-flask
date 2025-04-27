from flask import Flask
from config import Config
from extensions import db
from controllers.auth_controller import auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(auth_bp)


    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
