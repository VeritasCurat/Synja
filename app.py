'''
Created on 20.01.2019
@author: Johannes Grobelski
@version: 1.0

Webapp fuer Synja
@summary: Allgemeine Funktionsweise:
- Startet Webapp unter IP, rendert HTML's wenn nutzer auf die entsprechede route geht.
  indexSynja2.html (client) sendet per socket.emit(X,JSON) nachrichten an server @socketio.on(X, namespace='...') und erstellt synja bei connect (connect), schickt diese an synjaweb weiter (dialogeingabe_synja, lehreingabe_synja) etc.
  background_threadSynja wartet auf neue ausgaben von synjaweb (queues)und sendet diese per socketio.emit(X,JSON).
'''
import os
import sys
import time



path2 = os.path.realpath(__file__)[:-26]
print(path2)
sys.path.append(path2)

from threading import Lock
from flask import Flask, render_template, session, request
#from project.webapp.flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from project.webapp.SynjaWeb2 import Synja
import datetime


from project.webapp.usergate.usergate import Usergate
from flask.helpers import url_for
from builtins import isinstance


async_mode = None

app = Flask(__name__, static_url_path="/static")
app.config['SECRET_KEY'] = 'asde24oyx58ci6ad3skgr91ua2wp3oasd'
socketio = SocketIO(app, async_mode=async_mode)

thread = None
thread_lock = Lock()

thread_list = []
connections = []
synjas = []
synja_newusers = []

lizas = []

usergate = Usergate()
time_user = {}

logins = {} #ip -> [name, password]; None falls nicht eingeloggt
print("webapp ready!")

@app.route('/')
def render_indexSynja():
    return render_template('indexSynja2.html', async_mode=socketio.async_mode) 

@app.route('/about')
def render_about():
    return render_template('about-us.html', async_mode=socketio.async_mode)
  
@app.route('/how-to-use')
def render_howtouse():
    return render_template('how-to-use.html', async_mode=socketio.async_mode)
  
def background_threadSynja():
    count = 0
    current = int(round(time.time()))
    while True:
      count += 1
      #socketio.emit('my_response',
      #              {'data': 'Server generated event', 'count': count},
      #              namespace='/synja', room = connections[0])
      socketio.sleep(0.01)
      for synja in synjas:
        synja.nutzer_auf_inputfeld_hinweisen()
        #if(count%100==0):
        #  print(str(count/100))
        #  synja.lehrmanager.inc_responseTimer()
        if(synja.highlight_input_element == "lehre"): socketio.emit('highlight_lehre_input',namespace='/synja', room = synja.id)
        elif(synja.highlight_input_element == "dialog"): socketio.emit('highlight_dialog_input',namespace='/synja', room = synja.id)
        else: socketio.emit('highlight_no_input',namespace='/synja', room = synja.id)
          
        if(not synja.sendqueueDialog.empty()):
          output = synja.getDialogSynja()
          #print("Synja: "+str(output))
          #print("WA EMIT: "+output+" from ["+synja.name+"]")
          if(not isinstance(output,list)):   
            zeitpunkt = datetime.datetime.now().strftime('%H:%M:%S')         
            socketio.emit('dialogEINGABE',{'data':  '<p align="left"><b>Synja</b> ('+zeitpunkt+'): \n'+output+'</p>', 'count': count},namespace='/synja', room = synja.id)
            emotion = synja.lehrmanager.emotion
            socketio.emit('change_synja',{'data': emotion, 'count': count},namespace='/synja', room = synja.id)
           
          else:
            lehre = output[0]
                      
            #print("sending something out")
            #output = synja.sendqueueLehre.get()
            #print("WA: ART"+output[1])
            zeitpunkt = datetime.datetime.now().strftime('%H:%M:%S')         
            if(output[1] == "Task"): socketio.emit('lehrTASK',{'data': lehre, 'count': count},namespace='/synja', room = synja.id)
            elif(output[1] == "Lehre"): 
              if(lehre.endswith(".svg")):
                socketio.emit('lehrEINGABE_BILD',{'data': lehre, 'count': count},namespace='/synja', room = synja.id)
              else: socketio.emit('lehrEINGABE',{'data': lehre, 'count': count},namespace='/synja', room = synja.id)
        #check if user has underlined text
        socketio.emit('underline_checkS', {}, namespace='/synja', room=synja.id)

        count += 1
        
      if(int(round(time.time())) - current >= 1):
        current = int(round(time.time()))
        for s in synjas:
          socketio.emit('time',{},namespace='/synja', room = s.id)
               

@socketio.on('dialogeingabe', namespace='/synja')
def dialogeingabe_synja(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    zeitpunkt = datetime.datetime.now().strftime('%H:%M:%S')
    name = 'You'
    for synja in synjas:
        if synja.id == request.sid:
          if(synja.name != "NO_ACCOUNT"): name = synja.name
    emit('dialogEINGABE',{'data': '<b>'+name+'</b> ('+zeitpunkt+'): \n'+message['data'], 'count': session['receive_count']})
    #print("You: "+message['data'])
    #print("received \""  + message['data'] + "\" from " + request.sid)
    if (len(message['data']) > 0):
      for synja in synjas:
        if synja.id == request.sid:
          #print("WA de: "+message['data']+" from ["+str(synja.name)+"]")
          synja.addDialogNutzer(message['data'])
          synja.input = True
          
@socketio.on('lehreingabe', namespace='/synja')
def lehrausgabe_synja(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('dialogEINGABE',{'data': 'You: \"'+message['data'] + '\"', 'count': session['receive_count']})
    #print("received \""  + message['data'] + "\" from " + request.sid)
    if (len(message['data']) > 0):
      for synja in synjas:
        if synja.id == request.sid:
          synja.addLehreNutzer(message['data'])
          synja.input = True
    
@socketio.on('my_broadcast_event', namespace='/synja')
def broadcast_message_synja(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)


@socketio.on('join', namespace='/synja')
def join_synja(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.on('leave', namespace='/synja')
def leave_synja(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.on('close_room', namespace='/synja')
def close_synja(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.',
                         'count': session['receive_count']},
         room=message['room'])
    close_room(message['room'])


@socketio.on('my_room_event', namespace='/synja')
def send_room_message_synja(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         room=message['room'])


@socketio.on('disconnect_request', namespace='/synja')
def disconnect_request_synja():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    for synja in synjas:
        if synja.id == request.sid:
          synja.save()
    disconnect()

  
@socketio.on('logout', namespace='/synja')
def logout_synja():
    if(request.remote_addr in logins.keys()):
      logins.pop(request.remote_addr)
      emit('redirect', {'url': url_for('render_main')}) 
      for synja in synjas:
        if synja.id == request.sid:
          synja.save()

@socketio.on('connect', namespace='/synja')
def connect_synja():
    
    if(request.sid not in connections):
      connections.append(request.sid)
      #print("New connection: " + request.sid)
    
    #print("WA neuer Nutzer: "+str(name)+" "+request.remote_addr)
    name = "NO_ACCOUNT"
    nr = len(synjas)+1    
    Synja_ = Synja(request.sid, nr, name)

    if(str(name) in synja_newusers): Synja_.lehrmanager.neuernutzer = True
    thread_list.append(Synja_)
    synjas.append(Synja_)
    Synja_.start()
    global thread
    with thread_lock:
        if thread is None:
            emit('hinweis',{}, room=request.sid)
            thread = socketio.start_background_task(target=background_threadSynja)
    #emit('my_response', {'data': 'Connected\n', 'count': 0})         
        
@socketio.on('disconnect', namespace='/synja')
def disconnect_synja():
    print('Client disconnected', request.sid)
    for synja in synjas:
      if synja.id == request.sid:
        print("set to stop")
        synja.running = False
        synja.running = False
        
    
@socketio.on('my_ping', namespace='/synja')
def ping_pong_synja():
    emit('my_pong')        
        
        
if __name__ == '__main__':
  #s = serve(app, host='127.0.0.1', port=80)
  socketio.run(app)