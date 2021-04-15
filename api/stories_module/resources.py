from flask import Blueprint, request, jsonify
from enum import Enum
from http import HTTPStatus
from . import state_machine as stories_sm


from PIL import Image
import io, sys


stories_resources = Blueprint('stories_resources', __name__)

@stories_resources.route('', methods=['POST'], strict_slashes=False)
def insert_stories():
    file = request.files.get('file')
    grapher_name = request.form.get('grapher_name')

    if file is None:
        return jsonify({'message': 'file is missing'}), HTTPStatus.BAD_REQUEST

    if grapher_name is None:
        return jsonify({'message': 'grapher_name is missing'}), HTTPStatus.BAD_REQUEST
    
    story = stories_sm.insert(grapher_name, file)
    return story, HTTPStatus.OK

@stories_resources.route('', methods=['GET'], strict_slashes=False)
def get_all_stories():
    stories = stories_sm.get_all_stories()
    return stories, HTTPStatus.OK

@stories_resources.route('/<id>', methods=['GET'], strict_slashes=False)
def get_story(id):
    story = stories_sm.get_by_id(id)
    file = story.file
    print(sys.getsizeof(file))

    return jsonify({'message': 'fine'}), HTTPStatus.OK
