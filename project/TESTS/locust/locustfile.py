'''
Created on 31.05.2019

@author: Johannes
'''
from locust import HttpLocust, TaskSet

def enterSynja(l):
    l.client.post("/synja", {})

def index(l):
    l.client.get("/")

def profile(l):
    l.client.get("/profile")

class UserBehavior(TaskSet):
    tasks = {index: 2, profile: 1}

    def on_start(self):
      enterSynja(self)

   

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000