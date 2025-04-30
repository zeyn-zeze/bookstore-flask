from flask import Flask
from config import Config
from extensions import db,migrate
from controllers.auth_controller import auth_bp
from controllers.book_controller import book_bp
from controllers.user_controller import user_bp
from controllers.cart_controller import cart_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(auth_bp)
    app.register_blueprint(book_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(cart_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
