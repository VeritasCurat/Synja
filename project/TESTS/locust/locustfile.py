'''
Created on 31.05.2019

@author: Johannes
command: $ locust -f locustfile.py --host=141.20.25.57
'''
from locust import HttpLocust, TaskSet, task
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from socketIO_client import SocketIO, LoggingNamespace

import random
import string
import socketio
import json


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.enter_synja()

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        1+1

    

    def enter_synja(self):
        self.client.post("/testsynja", {})
        '''
        lehre1 = "TESTLEHRE"
        count1 = random.randint(0,100)
        room1 = random.randint(10000,20000)
        #self.client.post("/testsynja",{'data': lehre1, 'count': count1})
        
        data = {}
        data[""] = "bla"
        j  = json.dumps(data)
        socketIO.emit('lehreingabe', j)
        '''
      
        socketIO = SocketIO('141.20.25.57', 80, LoggingNamespace)
      
        randomstring = randomString()
        data = {'data': randomstring}
        j  = json.dumps(data)
                        
        socketIO.emit('dialogEINGABE',j)
      
    @task(2)
    def index(self):
        self.client.get("/")

    @task(1)
    def profile(self):
        self.client.get("/testsynja")

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
   
   


    