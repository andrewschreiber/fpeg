#!/usr/bin/env python

import os
import bottle
import logging
import urlparse

from messages import  MessageDB, MessageEncoder, MessageQueue

from bottle import route, get


import json

STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static')

logging.basicConfig()
log = logging.getLogger('receiver')
log.setLevel(logging.DEBUG)


log.debug("setting up message queue and db connection...")

try:
    mysql_url = urlparse.urlparse(os.environ['MYSQL_URL'])
except KeyError:
    log.warn("env variable MYSQL_URL not found, reverting to DATABASE_URL")
    mysql_url = urlparse.urlparse(os.environ['DATABASE_URL'])

rabbit_url = os.environ['RABBITMQ_URL']
queue_name = os.environ['QUEUE_NAME']

print os.environ['MYSQL_URL']
print os.environ['RABBITMQ_URL']

#rdb = redis.Redis(host=url.hostname, port=url.port, password=url.password)

url = mysql_url.hostname
password = mysql_url.password
user = mysql_url.username
dbname = mysql_url.path[1:] 


messageDB = MessageDB(url,dbname,user,password)
messageQueue = MessageQueue(rabbit_url)
messageQueue.getMessagesAsync(queue_name)
    
@get('/received') 
def getReceived():
    
    log.debug("handling /received path")

    #Gets messages, if method_frame decodes and adds to db
    #messageQueue.getMessages(queue_name,100)
    
    all_messages = messageDB.getMessages()
    
    return json.dumps(all_messages,cls=MessageEncoder)

'''
view routes
'''

@route('/')
def home():
	bottle.TEMPLATE_PATH.insert(0, './receiver_fpeg/views')
	return bottle.template('home')


@route('/static/:filename')
def serve_static(filename):
    log.debug("serving static assets")
    return bottle.static_file(filename, root=STATIC_ROOT)

'''
service runner code
'''
log.debug("starting web server")
application = bottle.app()
application.catchall = False

"""
#UNCOMMENT BELOW FOR RUNNING ON LOCALHOST
if os.getenv('SELFHOST', False):

url = os.getenv('VCAP_APP_HOST')
port = int(os.getenv('VCAP_APP_PORT'))
bottle.run(application, host=url, port=port)

#UNCOMMENT BELOW FOR RUNNING ON HDP
"""

bottle.run(application, host='0.0.0.0', port=os.getenv('PORT', 8080))


# this is the last line
