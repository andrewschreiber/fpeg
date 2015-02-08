

HP PaaS RabbitMQ Sender - sample code that sets up a web server that sends messages to a rabbitMQ topic

required ENV variables: 

these are supplied for you in HP Development Platform Application Lifecycle Service: 

RABBIT_URL
VCAP_APP_HOST
VCAP_APP_PORT

this one you need to fill out (make sure it matches the one in receiver project)
QUEUE_NAME


Note that the format of messages sent is as follows: 
{
    "sequence_id":3
    "sequence_value":2
}

where sequence_id maps to the id in the Fibonacci sequence, and sequence_value is the associated value in the series

1,1,2,3,5,8,13,21,34...




=======
sender
======

This is the sender for the HP Helion messaging demo

