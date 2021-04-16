from service import db
from core.models import Story
from task.tasks import process_image, process_video
from libs import helpers
from datetime import datetime
from sqlalchemy.orm import load_only, defer
from sqlalchemy import desc
import json

EXPOSED_FIELDS = ['id', 'created_at', 'grapher_name', 'name', 'description', 'state', 'file_type']

def get_by_id(story_id):
    story = Story.query.filter(Story.id == story_id).first()
    return story if story is not None else None


def get_all_stories():
    stories = Story.query.options(defer('file')).order_by(desc(Story.created_at)).all()
    return stories[0].serialize()

def insert(grapher_name, file):

    # story metadata information 
    story = Story()
    story.id = helpers.generate_id('st')
    story.created_at = datetime.utcnow()
    story.grapher_name = grapher_name
    story.name = file.filename
    story.file_type = file.mimetype.split('/')[0]
    story.description = 'This is a sample description'
    story.file = file.read()

    db.session.add(story)
    db.session.commit()

    story = get_by_id(story.id)

    # Removing file from the story object since it will result in increasing the size of payload
    del story.file

    # Checking the type and enqueueing a job
    if story.file_type == 'image':
        process_image.delay(story.id)
    elif story.file_type == 'video':
        process_video.apply_async(args=[story.id], countdown=1)

    return story.serialize()