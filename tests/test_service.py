import json
import pytest
from service.server import app
from core.models import Story
from celery_tasks.tasks import resize_image, resize_video

@pytest.fixture
def client():
    return app.test_client()


def test_service_ready(client):
    res = client.get('/ready')
    assert res.status_code == 200
    expected = {"message": "Service is ready!"}
    assert expected == json.loads(res.get_data(as_text=True))


def test_get_stories(client):
    res = client.get('/stories')
    assert res.status_code == 200


def test_post_story_grapher_name_missing(client):
    data = {
        'file': 'sample'
    }
    res = client.post('/stories', data=data, content_type='multipart/form-data')
    assert res.status_code == 400


def test_post_story_file_missing(client):
    data = {
        'grapher_name': 'Prashant'
    }
    res = client.post('/stories', data=data, content_type='multipart/form-data')
    assert res.status_code == 400


def test_process_image(client):
    test_file = open('tests/test_image.png', 'rb')
    result = resize_image(test_file.read(), 1200, 600)
    assert result is not None


def test_process_video(client):
    test_file = open('tests/test_video.mp4', 'rb')
    result = resize_video('st123', test_file.read(), 640)
    assert result is not None


def test_story_object_init(client):
    story = Story(id = 'st123', grapher_name = 'Prashant', name = 'Test.png', description = 'This is test', 
                    duration = 3600, file_type = 'image', state = 'UPLOADED')

    assert story.id == 'st123'
    assert story.grapher_name == 'Prashant'
    assert story.name == 'Test.png'
    assert story.description == 'This is test'
    assert story.duration == 3600
    assert story.file_type == 'image'
    assert story.state == 'UPLOADED'