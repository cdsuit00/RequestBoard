from flask import Flask
from backend.extensions import db, migrate, jwt, cors
from backend.routes import api
from backend import models
from backend.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)

    # Register blueprint
    app.register_blueprint(api, url_prefix="/api")

    # Ping route
    @app.route("/api/ping")
    def ping():
        return {"message": "pong"}

    return app
