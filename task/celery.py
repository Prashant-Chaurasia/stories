from celery import Celery
from service import app
import os

def make_celery(app):
    app.config['CELERY_BROKER_URL'] = os.environ.get('REDIS_URL', 'amqp://localhost:5672')
    # app.config['CELERY_RESULT_BACKEND'] = app.config['CELERY_BROKER_URL']
    # create context tasks in celery
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'], include=['task.tasks'])
    celery.conf.update(app.config)
    
    # TaskBase = celery.Task
    # class ContextTask(TaskBase):
    #     abstract = True
    #     def __call__(self, *args, **kwargs):
    #         with app.app_context():
    #             return TaskBase.__call__(self, *args, **kwargs)
    
    # celery.Task = ContextTask
    return celery

celery_app = make_celery(app)


# celery_app = Celery('background_tasks',
#              broker='amqp://localhost:5672',
#              include=['task.tasks'])

# celery_app.conf.update(app.config)

# if __name__ == '__main__':
#     celery_app.start()