from service import app, db
import json
from flask import jsonify, request
from api.stories_module import stories_resources

@app.after_request
def add_header(response):
    response.headers['Content-type'] = 'application/json'
    return response

@app.route('/ready', methods = ['POST'])
def index():
    response = jsonify({"message": "Service is ready!"})
    return response

# Any url with /stories will be routed to the stories_resources
app.register_blueprint(stories_resources, url_prefix='/stories')