from email.mime.text import MIMEText
from os.path import splitext
import smtplib
from subprocess import check_output
from uuid import uuid4

from celery import Celery

#---------- RabbitMQ Credentials ----------#
rabbitUser = 'rabbitUser'
rabbitPass = 'rabbitPass'
rabbitHost = 'localhost'
rabbitPort = 5672
rabbitVHost = 'rabbitVHost'

#---------- Celery Config ----------#
app = Celery('tasks')
app.conf.update(
    {
        'BROKER_URL':               'amqp://{0}:{1}@{2}:{3}/{4}'.format(rabbitUser, rabbitPass, rabbitHost, rabbitPort, rabbitVHost),
        'CELERY_RESULT_BACKEND':    'redis://localhost/0',
        #'CELERY_TASK_SERIALIZER':   'json',
        #'CELERY_RESULT_SERIALIZER': 'json',
        #'CELERY_ACCEPT_CONTENT':    ['json']
    })

#---------- Tasks ----------#
@app.task
def add(x, y):
    """
    Sum the 2 variables together. This is the "hello world" in celery universe.
    """
    return x + y

@app.task
def runUnitTest():
    """
    """
    result = check_output(['python', '-m', 'unittest', '-v', 'RunUnitTests'])
    return result

@app.task
def sendEmails(*addrs):
    """
    """
    SMTPUSER = 'user'
    SMTPPASS = 'pass'

    msg = MIMEText('Hello World')
    msg['Subject'] = 'Hello World'
    msg['From'] = 'user@yahoo.com'
    msg['To'] = 'user@gmail.com'

    print('port: %d' % 587 )
    s = smtplib.SMTP('smtp.mail.yahoo.com', port=587)
    s.starttls()
    s.login(SMTPUSER, SMTPPASS)
    s.send_message(msg)
    s.quit()
    return s

@app.task
def resizeImage(src, dest, height=50, width=50):
    """
    """
    with open(dest, 'wb') as f:
        f.write(src)

    filename, ext = splitext(dest)
    check_output(['convert', dest, '-resize', '%dx%d' % (height, width), '%s%s' % (uuid4(), ext)])
    

