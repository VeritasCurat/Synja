'''
Created on 31.05.2019

@author: Johannes
command: $ locust -f locustfile.py --host=141.20.25.57
'''
from locust import HttpLocust, TaskSet, task
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect

import random
import string

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
        emit('lehrTASK',{'data': lehre1, 'count': count1},namespace='/synja', room = room1)
        
        name2 = "john_doe_"+str(random.randint(0,10000))
        message2 = randomString(100)
        count2 = random.randint(0,100)
        emit('dialogEINGABE',{'data': '<b>'+name2+'</b>: \n'+message2, 'count': count2})
        '''
      
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