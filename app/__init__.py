from flask import Flask
from .extensions import db, migrate, login_manager, cors
from .api import auth_routes, photo_routes, message_routes
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    cors.init_app(app)

    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(photo_routes.bp)
    app.register_blueprint(message_routes.bp)

    return app
