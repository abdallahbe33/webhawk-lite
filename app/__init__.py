import os
from app import models
from flask import Flask
from app.routes.security_routes import security_bp
from app.config import DevelopmentConfig, config_by_name
from app.extensions import db, migrate
from app.routes.health_routes import health_bp
from app.routes.auth_routes import auth_bp
from app.routes.backend_routes import backend_bp
from app.routes.analytics_routes import analytics_bp
from app.routes.proxy_routes import proxy_bp


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



    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp,url_prefix="/auth",)

    app.register_blueprint(backend_bp,url_prefix="/backends",)
    app.register_blueprint(security_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(proxy_bp, url_prefix="/proxy")
    return app