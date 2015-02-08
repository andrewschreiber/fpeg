#!/usr/bin/env python

import os
import bottle
import logging

from bottle import route, request,post, template
import  pika
import threading
from time import sleep
import json
import psutil

STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static')

logging.basicConfig(format="%(threadName)s:%(thread)d:%(message)s")
log = logging.getLogger('sender')
log.setLevel(logging.DEBUG)


log.debug("setting up message queue")

rabbit_url = os.environ['RABBITMQ_URL']
queue_name = os.environ['QUEUE_NAME']
async_cpu = os.environ['ASYNC_CPU']

log.debug("rabbit mq url:%s"%os.environ['RABBITMQ_URL'])



def asyncCPUTest():
	log.debug("starting async CPU test method")
	while (1):
		sleep(5)
		log.debug("CPU percent = %d"%(psutil.cpu_percent()))
	
	
if (async_cpu != None) and async_cpu == "1":
	keepGoing = True
		
	"""
	sets up the async message processing thread, passing it the queue name to listen on
	"""
	log.debug("spawning async CPU loadtest thread")
	d = threading.Thread(name='sender-daemon', target=asyncCPUTest, args = ())
	d.setDaemon(True)
	d.start()



'''
view routes
'''
@post('/send') 
def send():
	number = request.json['number']
	if not number:
		return template('Please add a number to the end of url: /send/5')
	fib = F(int(number))
	#rabbit_url = os.environ['RABBITMQ_URL']
	parameters = pika.URLParameters(rabbit_url)
	connection = pika.BlockingConnection(parameters)
	channel = connection.channel() 
	channel.queue_declare(queue=queue_name)

	json_body = json.dumps({'sequence_id':int(number), 'sequence_value':int(fib)})
	 
	channel.basic_publish(exchange='', routing_key='fibq', body=json_body)
	connection.close()
	return json_body

def F(n):
	if n == 0: return 0
	elif n == 1: return 1
	else: return F(n-1)+F(n-2)

@route('/')
def home():
	bottle.TEMPLATE_PATH.insert(0, './sender_fpeg/views')
	return bottle.template('home', sent=False, body=None)

@post('/fib') 
def fib():
	number = request.json['number']
	if not number:
		return template('Please add a number to the end of url: /fib/5')
	fib = F(int(number))
	json_body = json.dumps({'sequence_id':int(number), 'sequence_value':int(fib)})
	return json_body


'''
Adding this route for use with StormRunner (to automate load, compute utilization)
'''

@route('/fib/<number:int>') 
def fib_num(number):
	if not number:
		return template('Please add a number to the end of url: /fib/5')
	fib = F(int(number))
	json_body = json.dumps({'sequence_id':int(number), 'sequence_value':int(fib)})
	return json_body


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
