#!/usr/bin/env python
import pika

class RabbitmqQueue:
    def __init__( self, hosts, user, password, queue ):
        self._hosts = hosts
        self._user = user
        self._password = password
        self._queue = queue
        self._connection = None
        self._channel = None
        self._connected = False
        self._connect()

    def _connect( self ):
        if self._connected:
            return True

        for host in self._hosts:
            if self._doConnect( host[0], host[1] ):
                return True

        return self._connected

    def _doConnect( self, host, port ):
        try:
            credentials = pika.PlainCredentials( self._user, self._password )
            parameters = pika.ConnectionParameters( host, port, "/", credentials )
            self._connection = pika.BlockingConnection( parameters )
            self._channel = self._connection.channel()
            self._channel.queue_declare( queue = self._queue )
            self._connected
            return True
        except:
            return False


    def publish( self, body ):
        for i in range(1):
            if not self._connected:
                self._connect()
            if self._publish( body ):
                return True
        return False

    def _publish( self, body ):
        try:
            self._channel.basic_publish( exchange = '',
                                routing_key = self._queue,
                                body = body )
            return True
        except:
            return False

    def close( self ):
       if self._connected:
            self._connected = False
            self._connection.close() 

    def consume( self, callback ):
        while True:
            if not self._connected:
                self._connect()
            self._consume( callback )

    def _consume( self, callback ):
        try:
            self._channel.basic_consume( callback, queue = self._queue, no_ack = True )
            self._channel.start_consuming()
        except:
            self.close()
        

"""
credentials = pika.PlainCredentials('nls', 'nls72NSN')
parameters = pika.ConnectionParameters('192.168.122.63', 5672, '/', credentials)
connection = pika.BlockingConnection( parameters )
channel = connection.channel()
channel.queue_declare(queue='hello')
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")

def callback(ch, method, properties, body):
    print body

queue = RabbitmqQueue( [("192.168.122.63", 5672), ("192.168.122.20", 5672)], "nls", "nls72NSN", "hello")
if queue.publish( "this is a test"):
    print "succeed to publish"
else:
    print "fail to publish"

queue.consume( callback )
"""
