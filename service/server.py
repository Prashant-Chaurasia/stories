from service import app, db
import json
from flask import jsonify, request

@app.after_request
def add_header(response):
    response.headers['Content-type'] = 'application/json'
    return response

@app.route('/ready', methods = ['POST'])
def index():
    response = jsonify({"message": "Service is ready!"})
    return response


from api.stories_module import stories_resources 
app.register_blueprint(stories_resources, url_prefix='/stories')