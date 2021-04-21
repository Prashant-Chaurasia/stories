from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from celery import Celery
from .config import Config
import os, json

def create_app():
    app = Flask(__name__)
    CORS(app, resources=r'/*', supports_credentials=True)
    app.config.from_object(Config)
    return app


def create_celery(app):
    app.config['CELERY_BROKER_URL'] = os.environ['REDIS_URL']
    # create context tasks in celery
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'], include=['celery_tasks.tasks'])
    celery.conf.update(app.config)
    return celery


app = create_app()
db = SQLAlchemy(app)
celery_app = create_celery(app)


@app.after_request
def add_header(response):
    response.headers['Content-type'] = 'application/json'
    return response


@app.route('/ready', methods = ['GET'])
def index():
    response = jsonify({"message": "Service is ready!"})
    return response


# Any url with /stories will be routed to the stories_resources
from api.stories_module import stories_resources
app.register_blueprint(stories_resources, url_prefix='/stories')