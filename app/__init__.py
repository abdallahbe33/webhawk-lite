import os

from flask import Flask

from app.config import DevelopmentConfig, config_by_name
from app.extensions import db, migrate
from app.routes.health_routes import health_bp
from app.routes.auth_routes import auth_bp
from app.routes.backend_routes import backend_bp

def create_app(config_name=None):
    app = Flask(__name__)

    environment = config_name or os.getenv(
        "APP_ENV",
        "development",
    )

    configuration = config_by_name.get(
        environment,
        DevelopmentConfig,
    )

    app.config.from_object(configuration)

    db.init_app(app)
    migrate.init_app(app, db)

    from app import models

    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp,url_prefix="/auth",)

    app.register_blueprint(backend_bp,url_prefix="/backends",)
    return app