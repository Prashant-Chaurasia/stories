from core.models import Story
from service.server import app, db, celery_app
from PIL import Image
import io, os, sys
import moviepy.editor as mp
from core.libs.constants import State

# Function that is responsible to resize an image
def resize_image(image_file, resize_height, resize_width):
    image = Image.open(io.BytesIO(image_file))
    # .thumbnail keeps the aspect ratio same as the original image
    image.thumbnail((resize_height, resize_width))
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr


@celery_app.task
def process_image(story_id):
    with app.app_context():
        story = Story.query.filter(Story.id == story_id).first()
        story.file = resize_image(story.file, 1200, 600)
        story.state = State.PROCESSED.value
        db.session.commit()
    return True


# Function that is responsible to change the resolution of a video
def resize_video(story_id, video_file, height, width=None):
    # Making temporary files for processing
    tmp_unprocessed_path = f'test_{story_id}.mp4'
    tmp_processed_path = f'output_{story_id}.mp4'
    
    tmp_unprocessed_file = open(tmp_unprocessed_path, "wb")
    tmp_unprocessed_file.write(video_file)
    tmp_unprocessed_file.close()

    clip = mp.VideoFileClip(tmp_unprocessed_path)
    #According to moviePy documenation The width is then computed so that the width/height ratio is conserved.
    clip_resized = clip.resize(height = height) 
    clip_resized.write_videofile(tmp_processed_path)
    
    tmp_processed_file = open(tmp_processed_path, "rb")

    # Removing temporary files
    os.remove(tmp_unprocessed_path)
    os.remove(tmp_processed_path)
    return tmp_processed_file.read()


@celery_app.task
def process_video(story_id):
    with app.app_context():
        story = Story.query.filter(Story.id == story_id).first()
        story.file = resize_video(story_id, story.file, 640)
        story.state = State.PROCESSED.value
        db.session.commit()
    return True
