from .celery import celery_app
from core.models import Story

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
import sys

from service import app, db

from PIL import Image
import io

engine = create_engine(
    'postgresql://postgres:postgres@localhost:5432/stories', convert_unicode=True,
    pool_recycle=3600, pool_size=10)

db_session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))

@celery_app.task
def process_image(story_id):
    with app.app_context():
        story = Story.query.filter(Story.id == story_id).first()
        print(story)

        # story = db_session.query(Story).filter(Story.id == story_id).first()
        file = story.file
        print(sys.getsizeof(file))

        image = Image.open(io.BytesIO(file))
        
        # .thumbnail keeps the aspect ratio same as the original image
        image.thumbnail((1200, 600))

        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        print(sys.getsizeof(img_byte_arr))

        story.file = img_byte_arr
        db.session.commit()
    return True


@celery_app.task
def process_video(file):
    return True
