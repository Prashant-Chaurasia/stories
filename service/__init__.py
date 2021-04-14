from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from .config import app_config
import os 

db = SQLAlchemy()

def create_app(environment):
    app = Flask(__name__)
    # Understand
    CORS(app, resources=r'/*', supports_credentials=True)
    app.config.from_object(app_config[environment])
    db.init_app(app)
    return app

app = create_app(os.getenv('ENVIRONMENT'))
# app = create_app('development')
