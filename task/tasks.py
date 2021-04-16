from .celery import celery_app
from core.models import Story
from service import app, db
from PIL import Image
import io, os, sys
import moviepy.editor as mp

@celery_app.task
def process_image(story_id):
    with app.app_context():
        story = Story.query.filter(Story.id == story_id).first()
        image = Image.open(io.BytesIO(story.file))
        
        # .thumbnail keeps the aspect ratio same as the original image
        image.thumbnail((1200, 600))

        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        story.file = img_byte_arr
        db.session.commit()
    return True


@celery_app.task
def process_video(story_id):
    with app.app_context():
        story = Story.query.filter(Story.id == story_id).first()

        # Making temporary files for processing
        tmp_unprocessed_path = f'/tmp/test_{story.id}.mp4'
        tmp_processed_path = f'/tmp/output_{story.id}.mp4'
        
        tmp_unprocessed_file = open(tmp_unprocessed_path, "wb")
        tmp_unprocessed_file.write(story.file)
        tmp_unprocessed_file.close()

        clip = mp.VideoFileClip(tmp_unprocessed_path)
        #According to moviePy documenation The width is then computed so that the width/height ratio is conserved.
        clip_resized = clip.resize(height=640) 
        clip_resized.write_videofile(tmp_processed_path)
        
        with open(tmp_processed_path, "rb") as tmp_processed_file:
            data = tmp_processed_file.read()
            story.file = data
            story.state = 'PROCESSED'

        db.session.commit()

        # Removing temporary files
        os.remove(tmp_unprocessed_path)
        os.remove(tmp_processed_path)
    return True
