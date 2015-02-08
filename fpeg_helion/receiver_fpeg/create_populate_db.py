'''
Created on Sep 4, 2014

@author: jacoba
'''
import MySQLdb
import urlparse
import os
import logging

if __name__ == '__main__':
    
    try:
        logging.basicConfig()
        log = logging.getLogger('receiver')
        log.setLevel(logging.DEBUG)

        try:
            mysql_url = urlparse.urlparse(os.environ['MYSQL_URL'])
        except KeyError:
            log.warn("env variable MYSQL_URL not found, reverting to DATABASE_URL")
            mysql_url = urlparse.urlparse(os.environ['DATABASE_URL'])
    
        #rdb = redis.Redis(host=url.hostname, port=url.port, password=url.password)
        
        url = mysql_url.hostname
        password = mysql_url.password
        userName = mysql_url.username
        dbName = mysql_url.path[1:] # slice off the '/'
        db = MySQLdb.connect(host=url,user=userName,passwd=password,db=dbName)
        
        table_create = 'CREATE TABLE IF NOT EXISTS messages( message_id int not null auto_increment, sequence_id int not null, sequence_value bigint not null, created_date varchar(100),PRIMARY KEY(message_id));'
        
        cur = db.cursor()

        log.debug('executing table create')
        
        cur.execute(table_create)
        db.commit()
         

    except MySQLdb.Error, e:
        print "Exception during database initialization: %s"%str(e)
