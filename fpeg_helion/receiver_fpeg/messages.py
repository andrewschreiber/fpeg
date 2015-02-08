'''
Created on Nov 13, 2014

@author: arunjacob
'''
import MySQLdb
import json
import pika
import threading
import logging
import datetime
import urlparse
import os

logging.basicConfig()

class MessageEncoder(json.JSONEncoder):
        
    def default(self,o):
        return o.__dict__
    
messageLogger = logging.getLogger('message')
messageLogger.setLevel(logging.DEBUG)

class Message(object):
    '''
    contains sequence_id, sequence_value, created information.
    '''


    def __init__(self, row = None, details = None):
        


        if row != None:
            messageLogger.debug("initializing from database")
            
            self.message_id = row[0]
            self.sequence_id = row[1]
            self.sequence_value = row[2]
            self.created_date = row[3]
        elif details != None:
            messageLogger.debug("initializing from JSON")
            self.message_id = -1
            if details.has_key('sequence_id') == True:
                self.sequence_id = details['sequence_id']
            else:
                messageLogger.error("invalid JSON format, sequence_id not found")
                raise 'invalid format'
            
            if details.has_key('sequence_value') == True:
                self.sequence_value = details['sequence_value']
            else:
                messageLogger.error("invalid JSON format, sequence_value  not found")
                raise 'invalid format'    
            
            # created is optional. It's always overwritten on insert to db.
            if details.has_key('created_date'):
                self.created_date = details['created_date']
    
    
    
class MessageDB(object):
    
    def __init__(self,url,dbName,userName,password):
        
        self.log =  logging.getLogger('messageDB')
        self.log.setLevel(logging.DEBUG)
        self.url= url
        self.dbName = dbName
        self.userName = userName
        self.password = password
        
            
            
    def connectToDB(self):
        try:
            self.log.debug("connecting database")
            db = MySQLdb.connect(host=self.url,user=self.userName,passwd=self.password,db=self.dbName) 
            cur = db.cursor()
            cur.execute('use %s'%self.dbName)
            return db
        except MySQLdb.Error, e:
            self.log.error("unable to connect to database")
            self.handleMySQLException(e,True)
            return None
            
    def disconnectFromDB(self,db):
        try: 
            db.close()
            
        except MySQLdb.Error, e:
            self.log.error("unable to disconnect from database")
            self.handleMySQLException(e,True)
            
            
            
    def handleMySQLException(self,e,throwEx=False):
        """
        parses sql exceptions into readable format
        """
        try:
            self.log.error( "Error [%d]: %s"%(e.args[0],e.args[1]))
        except IndexError:
            self.log.error( "Error: %s"%str(e))
            
        raise e
    
    def addMessage(self,message):
        """
        inserts a message into the database and timestamps it for readability
        """
        try:
            db = self.connectToDB()
            cur = db.cursor()
            #created_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            created_date = unicode(datetime.datetime.now())
            self.log.debug("adding message into database with sequence_id = %d and sequence_value = %d and created_date = '%s'"%(message.sequence_id,message.sequence_value,created_date))
            query = "insert into messages(sequence_id, sequence_value,created_date) values(%d,%d,'%s')"%(message.sequence_id, message.sequence_value,created_date)
            cur.execute(query)
            db.commit()
            self.disconnectFromDB(db)
                
                
        except MySQLdb.Error as e:
            self.log.error(str(e))
            self.handleMySQLException(e)
       
       
    def getMessages(self,isDescending=True,limit = 100):
        """
        retrieves specified limit count of messages from database
        """
    
        msgs = []
        self.log.debug("retrieving messages, limit = %d"%limit)
        try:
            
            db = self.connectToDB()
            if isDescending == True:
                query = 'select message_id,sequence_id, sequence_value,created_date from messages order by message_id DESC LIMIT %d'%limit
            else:
                query = 'select message_id,sequence_id, sequence_value,created_date from messages order by message_id LIMIT %d'%limit # will order ASC because message_id is the primary key
            
            cur = db.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            
            for row in rows:
                msgs.append(Message(row))
                
            
        except MySQLdb.Error, e:
            self.handleMySQLException(e)
    
        self.disconnectFromDB(db)
        self.log.debug("returning %d messages"%len(msgs))
        return msgs
    

    def dropAllMessages(self):
        """
        for testing: truncate the db
        """
        self.log.debug("dropping all messages")
        try:
            db = self.connectToDB()
            query = "TRUNCATE TABLE messages"
            cur = db.cursor()
            cur.execute(query)
            db.commit()
            
        except MySQLdb.Error, e:
            self.log.error(str(e))
            self.handleMySQLException(e)
        
        self.disconnectFromDB(db)
            
class MessageQueue:
    def __init__(self,amqp_url):
        self.log =  logging.getLogger('messageQueue')
        self.log.setLevel(logging.DEBUG)
        self.amqp_url = amqp_url
        self.channel = None
        self.messageDB = None
    
        
    def getMessages(self, queue_name,messageCount):
        """
        pulls messages from the queue, for a specified count of messages
        """
        self.log.debug("getting %d messages from queue"%messageCount)
        parameters = pika.URLParameters(self.amqp_url)
        connection = pika.BlockingConnection(parameters)

        channel = connection.channel()
        i = 0
        
        for i in range(0,messageCount):
            
            method_frame, header_frame, body = channel.basic_get(queue_name)
            if method_frame:
                try:
                    self.log.debug("message %d, method frame = %s, header fraem = %s"%(i,method_frame,header_frame))
                    self.decodeAndAddMessage(body) 
                except:
                    self.log.error ("message %d, invalid format of message, removing message from queue"%i)
                
                channel.basic_ack(delivery_tag=method_frame.delivery_tag)
                    
            else:
                break
            
    def decodeAndAddMessage(self,messageBody):
        """
        adds the message to the database
        """
        messageContents = json.loads(messageBody)
    
        message = Message(None,messageContents)
        
        if(self.messageDB != None):
            self.messageDB.addMessage(message)
        else:
            logging.error("unable to add message, DB connection has not been initialized yet")
        
                
    def getMessagesAsync(self,queue_name):
        """
        sets up the async message processing thread, passing it the queue name to listen on
        """
        self.log.debug("spawning async message processing thread")
        d = threading.Thread(name='daemon', target=self.asyncMessageConsumption, args = (queue_name,))
        d.setDaemon(True)
        d.start()
        
    
    def asyncMessageConsumption(self,queue_name):
        
        """
        spawned async and handles putting data into the database. 
        """
        mysql_url = urlparse.urlparse(os.environ['MYSQL_URL'])
        
        url = mysql_url.hostname
        password = mysql_url.password
        user = mysql_url.username
        dbname = mysql_url.path[1:] 
        
        self.log.debug("starting messageDB instance on separate thread.")
        self.messageDB = MessageDB(url,dbname,user,password)
        self.log.debug("started messageDB instance on separate thread.")
        self.log.debug("async message processing thread, setting up RabbitMQ Connection")
        parameters = pika.URLParameters(self.amqp_url)
        connection = pika.BlockingConnection(parameters)

        channel = connection.channel()
        try:
            self.log.debug("kicking off channel creation...")
            #I believe queue_declare will only create the queue if doesn't already exist.
            channel.queue_declare(queue=queue_name)
            channel.basic_consume(self.on_message, queue_name)
            self.log.debug("starting to consume messages...")
            channel.start_consuming()
        except Exception, err:
            print Exception, err

        # note that this should probably be part of a cleanup method that gets invoked as part of thread shutdown.
        channel.stop_consuming()
        connection.close()
        self.log.debug("finished consuming messages...")
        
        
    def on_message(self,channel, method_frame, header_frame, body):
        """
        called as part of basic_consume semantics, when messages are received.
        """
        self.log.debug("processing asynchronously received message")
        try:
            self.decodeAndAddMessage(body) 
        except:
            print 'This is the body!! Why is this invalid?'
            print method_frame
            print header_frame
            print body
            self.log.error ("invalid format of message, removing message from queue")
                
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        
    
        