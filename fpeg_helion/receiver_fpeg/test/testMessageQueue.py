'''
Created on Nov 14, 2014

@author: arunjacob
'''
import unittest
import urlparse
import os
import pika
import time

from messages import Message,MessageEncoder, MessageDB, MessageQueue
from testUtils import initializeMessageDB, initializeMessageQueue
class Test(unittest.TestCase):


    def pushMessage(self,rabbit_url,topic):
        parameters = pika.URLParameters(rabbit_url)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        
        #channel.queue_declare(queue='hello2')
        
        channel.basic_publish(exchange='',
            routing_key= topic,
            body = '{"sequence_id":3, "sequence_value":2}')
        connection.close()
        
#     def test1RunMessageQueue(self):
#         #10.8.50.235:5671/%2f
#         rabbit_url = "amqps://arun:arun@10.8.50.235:5671/%2f"
#         for i in range(0,5):
#             self.pushMessage(rabbit_url)
#         messageDB = initializeMessageDB()
#         messageQ = initializeMessageQueue(rabbit_url,messageDB)
#         messageQ.getMessages("hello",10)
        
        
#     def test2AsyncMessageQueue(self):
#         rabbit_url = "amqps://arun:arun@10.8.50.235:5671/%2f"
#         for i in range(0,5):
#             self.pushMessage(rabbit_url,"hello")
#  
#         messageDB = initializeMessageDB()
#         messageQ = initializeMessageQueue(rabbit_url,messageDB)
#         messageQ.getMessagesAsync("hello")
#         time.sleep(10)
        
        
    def testPushMessages(self):
        rabbit_url = "amqps://arun:arun@10.8.50.235:5671/%2f"
        for i in range(0,5):
            self.pushMessage(rabbit_url,"hello")
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()