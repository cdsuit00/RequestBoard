from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from backend.config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Import models so migrations detect them
    from backend import models  

    # Register blueprints
    from backend.routes import api
    app.register_blueprint(api, url_prefix="/api")

    return app
