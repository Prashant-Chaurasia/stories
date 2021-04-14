from service import app, db
import json
from flask import jsonify, request

@app.after_request
def add_header(response):
    response.headers['Content-type'] = 'application/json'
    return response

@app.route('/ready', methods = ['GET'])
def index():
    response = jsonify({"message": "Service is ready!"})
    return response

