from service.server import db
from core.models import Story
from celery_tasks.tasks import process_image, process_video
from core.libs import helpers, serializers
from datetime import datetime
from sqlalchemy.orm import defer
from sqlalchemy import desc
import json
from core.libs.constants import State


def get_by_id(story_id):
    story = Story.query.filter(Story.id == story_id).first()
    return story if story is not None else None


def get_all_stories():
    stories = Story.query.options(defer('file')).order_by(desc(Story.created_at)).all()
    return serializers.serialize(stories)


def enqueue_background_task(story):
    # Checking the type and enqueueing a job
    if story.file_type == 'image':
        process_image.delay(story.id)
    elif story.file_type == 'video':
        process_video.delay(story.id)


def update_story_object(story, data, file):
    story.id = helpers.generate_id('st')
    story.created_at = datetime.utcnow()
    for key, value in data.items():
        if hasattr(story, key) and value: 
            setattr(story, key, value)

    story.name = file.filename if story.name is None else story.name
    story.file_type = file.mimetype.split('/')[0] if story.file_type is None else story.file_type
    story.state = State.UPLOADED.value
    story.file = file.read()
    return story

def insert(file, data):
    # story metadata information and saving the story in the db 
    story = Story()
    story = update_story_object(story, data, file)
    db.session.add(story)
    db.session.commit()

    # Enqueuing background task to process image and video 
    enqueue_background_task(story)

    # returning the saved story object
    story = get_by_id(story.id)
    # Removing file from the story object since it will result in increasing the size of payload
    del story.file
    return serializers.serialize(story)
