'''
Created on Nov 14, 2014

@author: arunjacob
'''
import unittest
import urlparse
import os

from messages import Message,MessageEncoder, MessageDB
from testUtils import initializeMessageDB

class Test(unittest.TestCase):


   
        
    def test1InitializeMessage(self):
        
        messageDB = initializeMessageDB()
        message = Message(None,{"sequence_id":3, "sequence_value":2})
        messageDB.addMessage(message)

        msgs = messageDB.getMessages()
        
        self.assertTrue(msgs != None)

        self.assertTrue(len(msgs) > 0)
        
        
#     def test2DropAllMessages(self):
#         messageDB = self.initializeMessageDB()
#         messageDB.dropAllMessages()
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()