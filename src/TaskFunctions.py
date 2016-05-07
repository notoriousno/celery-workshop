from celery import Celery

#---------- RabbitMQ Credentials ----------#
rabbitUser = 'rabbitUser'
rabbitPass = 'password'
rabbitHost = 'localhost'
rabbitPort = 5672
rabbitVHost = 'rabbitVHost'

#---------- Celery Config ----------#
app = Celery('tasks')
app.conf.update(
    {
        'BROKER_URL':               'amqp://{0}:{1}@{2}:{3}/{4}'.format(rabbitUser, rabbitPass, rabbitHost, rabbitPort, rabbitVHost),
        'CELERY_RESULT_BACKEND':    'redis://localhost/0',
        'CELERY_TASK_SERIALIZER':   'json',
        'CELERY_RESULT_SERIALIZER': 'json',
        'CELERY_ACCEPT_CONTENT':    ['json']
    })

#---------- Tasks ----------#
@app.task
def add(x, y):
    """
    Sum the 2 variables together. This is the "hello world" in celery universe.
    """
    return x + y

