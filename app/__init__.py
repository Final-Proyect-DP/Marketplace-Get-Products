from flask import Flask
from .config.config import Config
from .extensions.extensions import db
from .controllers.product_controller import product_bp
from .routes.routes import read_bp
from flasgger import Swagger
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    Swagger(app, template_file="swagger_config.yaml")
    CORS(app)  # Enable CORS for all routes

    # Register Blueprints for the routes
    app.register_blueprint(product_bp)
    app.register_blueprint(read_bp)

    return app
