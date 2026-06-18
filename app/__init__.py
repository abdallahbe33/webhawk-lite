import os

from flask import Flask

from app.config import DevelopmentConfig, config_by_name
from app.routes.health_routes import health_bp


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

    app.register_blueprint(health_bp)

    return app