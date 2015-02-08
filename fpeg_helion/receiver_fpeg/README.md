receiver
========

HP PaaS RabbitMQ Receiver - sample code that sets up a web server that receives messages from a rabbitMQ topic and serializes them to the database. 

required ENV variables: 

these are supplied for you in HP Development Platform Application Lifecycle Service: 

MYSQL_URL
RABBIT_URL
VCAP_APP_HOST
VCAP_APP_PORT

this one you need to fill out (make sure it is the same one that people are pushing messages to)
QUEUE_NAME


Note that the format of messages sent is as follows: 
{
    "sequence_id":3
    "sequence_value":2
}

where sequence_id maps to the id in the Fibonacci sequence, and sequence_value is the associated value in the series

1,1,2,3,5,8,13,21,34...




