
import bottle
from bottle import route, request, post, template

import json
import os


@route('/')
def home():
  bottle.TEMPLATE_PATH.insert(0, './views')
  return bottle.template('home', sent=False, body=None)


@route('/compress')
def compress():
  pass



application = bottle.app()
application.catchall = False

bottle.run(application, host='0.0.0.0', port=os.getenv('PORT', 8080))
