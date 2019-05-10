import sys, time
import warnings
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
from multiprocessing.connection import Listener
from multiprocessing.connection import Client
import sys, time, select


class TimeoutExpired(Exception):
    pass

class UI:	

  def __init__(self):      
    print("--ui initialised--")

  def connect(self):
    address = ('localhost', 6000)
    conn = Client(address, authkey='secret password')
    conn.send('close')
    conn.close()

  def tell(self, phrase):
    print("sending")
    self.conn.send(phrase)
    
