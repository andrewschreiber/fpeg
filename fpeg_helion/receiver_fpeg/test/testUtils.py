'''
Created on Nov 14, 2014

@author: arunjacob
'''

import urlparse
from messages import MessageDB, MessageQueue

def initializeMessageDB():
        
    MYSQL_URL = "mysql://dev:devpass@localhost/receiverdb"
    
    mysql_url = urlparse.urlparse(MYSQL_URL)
    
    
    #rdb = redis.Redis(host=url.hostname, port=url.port, password=url.password)
    
    url = mysql_url.hostname
    password = mysql_url.password
    user = mysql_url.username
    dbname = mysql_url.path[1:] 
    
    messageDB = MessageDB(url,dbname,user,password)
    
    return messageDB

def initializeMessageQueue(rabbit_url):
        
    # this assumes a real external rabbit queue. TODO: create an internal version.
    
    #rdb = redis.Redis(host=url.hostname, port=url.port, password=url.password)
    
    
    
    messageQ = MessageQueue(rabbit_url)
    
    return messageQ