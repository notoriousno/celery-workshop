from hashlib import md5
from os import environ, mkdirs, path
import subprocess
from uuid import uuid4

from klein import Klein

app = Klein()

@app.route('/upload', methods=['POST'])
def upload(request):
    image = request.args.get(b'fileupload')[0]
    uploadDir = path.join(environ.get('HOME'), 'celery-workshop', 'dmz')

    if not path.exists(uploadDir):
        mkdirs(uploadDir)   # create dir if not exists

    randomID = str(uuid4()).replace('-', '')        # random name for the file
    dmzPath = path.join(uploadDir, randomID)
    with open(dmzPath, 'wb') as f:
        f.write(image)      # create the file

    uploadDest = '/some/path/to/save/resized/images'
    # process = subprocess.Popen(['convert', '-resize', ])

    md5hash = md5()
    with open(uploadDest, 'rb') as f:
        for chunk in iter(lambda: f.read(1024), b''):
            md5hash.update(chunk)
    md5hash = md5hash.hexdigest()

