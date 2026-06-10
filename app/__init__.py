import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Setup logging
    logging.basicConfig(level=app.config["LOG_LEVEL"])
    logger = logging.getLogger(__name__)
    logger.info("Starting Student API...")

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.routes.student import student_bp
    app.register_blueprint(student_bp, url_prefix="/api/v1")

    return app