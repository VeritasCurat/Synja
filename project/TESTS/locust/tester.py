'''
Created on 03.06.2019

@author: Johannes
'''
from locust import HttpLocust, TaskSet, task
#from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
#from socketIO_client import SocketIO, LoggingNamespace, BaseNamespace

import random
import string
import socketio
import json

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

if __name__ == '__main__':
    #socketIO = SocketIO('141.20.25.57', 80, LoggingNamespace)
    '''
    socketIO = SocketIO('127.0.0.1', 80, LoggingNamespace)
    print("test1")
    socketIO.define(BaseNamespace, '/synja')
    print("test2")
    '''
    socketIO = socketio.Client()
    socketIO.connect('http://127.0.0.1:80', namespaces=['/synja'])
    print("test1")
    
    randomstring = randomString()
    data = {'data': randomstring}
    #j  = json.dumps(data)
                    
    socketIO.emit('dialogeingabe',{'data': randomstring},namespace="/synja")
    print("test2")
    socketIO.disconnect()
