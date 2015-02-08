
import bottle
from bottle import route, request, post, template

import logging

import json
import os

logging.basicConfig()
log = logging.getLogger("fpeg")
log.setLevel(logging.DEBUG)

STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static')


@route('/')
def home():
  bottle.TEMPLATE_PATH.insert(0, './views')
  return bottle.template('home', sent=False, body=None)


@post('/compress')
def compress():
  data = request.files.get("upload")
  if data and data.file:
    raw = data.file.read()
    filename = data.filename
    log.debug("uploaded {} ({} bytes).".format(filename, len(raw)))
  else:
    log.error("upload failed")
        


@route('/static/:filename')
def serve_static(filename):
    log.debug("serving static assets")
    return bottle.static_file(filename, root=STATIC_ROOT)
    

application = bottle.app()
application.catchall = False

bottle.run(application, host='0.0.0.0', port=os.getenv('PORT', 8080))
