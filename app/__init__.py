import os

from flask import Flask, jsonify

from app.config import config_by_name
from app.config import DevelopmentConfig, config_by_name


def create_app(config_name=None):
    app = Flask(__name__)

    environment = config_name or os.getenv("APP_ENV", "development")
    configuration = config_by_name.get(
        environment,
        DevelopmentConfig,
    )

    app.config.from_object(configuration)

    @app.get("/health")
    def health():
        return jsonify(
            service="WebHawk Lite",
            status="ok",
            environment=app.config["APP_ENV"],
        )

    return app