from flask import Blueprint, request, jsonify
from enum import Enum
from http import HTTPStatus
from . import state_machine as stories_sm
from flask import send_file
from PIL import Image
import io
from core.libs.constants import default_duration, State

stories_resources = Blueprint('stories_resources', __name__)

@stories_resources.route('', methods=['POST'], strict_slashes=False)
def insert_stories():
    file = request.files.get('file')
    grapher_name = request.form.get('grapher_name')

    if file is None:
        return jsonify({'message': 'file is missing'}), HTTPStatus.BAD_REQUEST

    if grapher_name is None:
        return jsonify({'message': 'grapher_name is missing'}), HTTPStatus.BAD_REQUEST
    
    # Received attributes 
    data = {
        'grapher_name': grapher_name,
        'description': request.form.get('description'),
        'name': request.form.get('name'),
        'duration': request.form.get('duration', default_duration),
        'file_type': request.form.get('type'),
        'latitude': request.form.get('latitude'),
        'longitude': request.form.get('longitude')
    }
    
    story = stories_sm.insert(file, data)
    return story, HTTPStatus.OK

@stories_resources.route('', methods=['GET'], strict_slashes=False)
def get_all_stories():
    stories = stories_sm.get_all_stories()
    return stories, HTTPStatus.OK

@stories_resources.route('/<id>', methods=['GET'], strict_slashes=False)
def get_story(id):
    story = stories_sm.get_by_id(id)
    
    # Not returning the file till it is processed. 
    if (story.state == State.UPLOADED.value):
        return jsonify({'message': 'The story is being processed, please retry after sometime!'}), HTTPStatus.OK

    file = story.file
    return send_file(io.BytesIO(file), attachment_filename=story.name, as_attachment=True)
