'''
Created on 20.01.2019
@author: Johannes Grobelski
@version: 1.0

Webapp fuer Synja und Liza
@summary: Allgemeine Funktionsweise:
- Startet Webapp unter IP, rendert HTML's wenn nutzer auf die entsprechede route geht.
  indexSynja2.html (client) sendet per socket.emit(X,JSON) nachrichten an server @socketio.on(X, namespace='...') und erstellt synja bei connect (connect), schickt diese an synjaweb weiter (dialogeingabe_synja, lehreingabe_synja) etc.
  background_threadSynjaLiza wartet auf neue ausgaben von synjaweb (queues), liza und sendet diese per socketio.emit(X,JSON).
- Webapp speichert ob nutzer sich eingeloggt haben per ip-adresse
'''
import os
import sys
import time
#import gevent
#from engineio.async_drivers import eventlet
import datetime
from flask.helpers import url_for
from builtins import isinstance
from threading import Lock
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect  #@Unresolvedimport

print("libs ready!")


sys.path.append(os.path.abspath('../lehre/javaparsing'))
sys.path.append(os.path.abspath('../lehre'))
sys.path.append(os.path.abspath('.'))
from javaparser import parse,multiparse  #@Unresolvedimport
from SynjaWeb2 import Synja  #@Unresolvedimport
from verlauf import eintragen_load  #@Unresolvedimport
from liza.l import L  #@Unresolvedimport
from usergate.usergate import Usergate  #@Unresolvedimport
print("natives ready!")

async_mode = None
app = Flask(__name__) #, static_url_path="/static"
app.config['SECRET_KEY'] = 'asde24oyx58ci6ad3skgr91ua2wp3oasd'
socketio = SocketIO(app, async_mode=async_mode) #, async_mode=async_mode

thread = None
thread_lock = Lock()

thread_list = []
connections = []
synjas = []
lizas = []
print("webapp ready!")

@app.route('/synja_de')
def render_indexSynja_DE():
    return render_template('de/indexSynja2.html', async_mode=socketio.async_mode) 
    
@app.route('/synja_en')
def render_indexSynja_EN():
    return render_template('en/indexSynja2.html', async_mode=socketio.async_mode) 
   
@app.route('/liza')
def render_indexLiza():
    return render_template('en/indexLiza.html', async_mode=socketio.async_mode) 
    
@app.route('/en')
def render_mainEN():
    return render_template('en/main.html', async_mode=socketio.async_mode)
    
@app.route('/')
def render_mainDE():    
    return render_template('de/main.html', async_mode=socketio.async_mode)  
  
@app.route('/about')
def render_aboutEN():
    return render_template('en/about-us.html', async_mode=socketio.async_mode)
    
@app.route('/about')
def render_aboutDE():    
    return render_template('de/about-us.html', async_mode=socketio.async_mode)
    
@app.route('/how-to-use')
def render_howtouseEN():
    return render_template('en/how-to-use.html', async_mode=socketio.async_mode)
    
@app.route('/how-to-use')
def render_howtouseDE():    
    return render_template('de/how-to-use.html', async_mode=socketio.async_mode)
  

def background_threadSynjaLiza():
    count = 0
    eintragen_load(Synja.totalCount)

    loadtimer = 0
    while True:
      count += 1

      socketio.sleep(0.01)
      loadtimer += 1
      #if(loadtimer % 100 == 0):
        #print(len(synjas))
        #print(bgcount)
      if(loadtimer > 1000):
        eintragen_load(Synja.totalCount)
        loadtimer = 0
      
      for synja in synjas:  
        if(synja.running == False):
          try:
            synjas.remove(synja)
            del synja
            Synja.totalCount -= 1
          except:
            print("Could not delete synja!")
          continue
        try:    
          '''
          if(synja.lastmessagetime != None and synja.lastmessagetime != 0 and (int(round(time.time())) - synja.lastmessagetime) > 1200):
            try:

              if(synja.sprache=="de"):socketio.emit('dialogEINGABE',{'data':  '<p align="left"><b>Synja</b>: \n'+str("Du hast zu lange nicht mehr reagiert. Auf Wiedersehen! Bitte lade die Seite neu.")+'</p>', 'count': count},namespace='/synja_de', room = synja.id)
              else: socketio.emit('dialogEINGABE',{'data':  '<p align="left"><b>Synja</b>: \n'+str("You haven't reacted for too long. Good bye! Please reload the page.")+'</p>', 'count': count},namespace='/synja_en', room = synja.id)
              synja.running = False
              continue
            except Exception as ex:
              template = "An exception of type {0} occurred. Arguments:\n{1!r}"
              message = template.format(type(ex).__name__, ex.args)
                              
          #synja.nutzer_auf_inputfeld_hinweisen()
          '''
          
          
          if(synja.highlight_input_element == "lehre"): 
            if(synja.sprache=="de"): socketio.emit('highlight_lehre_input',namespace='/synja_de', room = synja.id)
            else: socketio.emit('highlight_lehre_input',namespace='/synja_en', room = synja.id)
          elif(synja.highlight_input_element == "dialog"): 
            if(synja.sprache=="de"): socketio.emit('highlight_dialog_input',namespace='/synja_de', room = synja.id)
            else: socketio.emit('highlight_dialog_input',namespace='/synja_en', room = synja.id)
          else:
            if(synja.sprache=="de"): socketio.emit('highlight_no_input',namespace='/synja_de', room = synja.id)
            else: socketio.emit('highlight_no_input',namespace='/synja_en', room = synja.id)
            
          if(not synja.sendqueueDialog.empty()):
            output = synja.getDialogSynja()
            #print("WA EMIT: "+output+" from ["+synja.name+"]")
            if(not isinstance(output,list)):   
              zeitpunkt = datetime.datetime.now().strftime('%H:%M:%S')         
              if(synja.sprache=="de"): socketio.emit('dialogEINGABE',{'data':  '<p align="left"><b>Synja</b>: \n'+output+'</p>', 'count': count},namespace='/synja_de', room = synja.id)
              else: socketio.emit('dialogEINGABE',{'data':  '<p align="left"><b>Synja</b>: \n'+output+'</p>', 'count': count},namespace='/synja_en', room = synja.id)
              emotion = synja.lehrmanager.emotion
              if(synja.sprache=="de"): socketio.emit('change_synja',{'data': emotion, 'count': count},namespace='/synja_de', room = synja.id) 
              else: socketio.emit('change_synja',{'data': emotion, 'count': count},namespace='/synja_en', room = synja.id) 
            else:
              lehre = output[0]
              zeitpunkt = datetime.datetime.now().strftime('%H:%M:%S')         
              if(output[1] == "Task"): 
                if(synja.sprache=="de"): socketio.emit('lehrTASK',{'data': lehre, 'count': count},namespace='/synja_de', room = synja.id)
                else: socketio.emit('lehrTASK',{'data': lehre, 'count': count},namespace='/synja_en', room = synja.id)
              elif(output[1] == "Lehre"): 
                if(lehre.endswith(".svg")):
                  if(synja.sprache=="de"): socketio.emit('lehrEINGABE_BILD',{'data': lehre, 'count': count, 'lang': synja.sprache},namespace='/synja_de', room = synja.id)
                  else: socketio.emit('lehrEINGABE_BILD',{'data': lehre, 'count': count, 'lang': synja.sprache},namespace='/synja_de', room = synja.id)
                else: 
                  if(synja.sprache=="de"): socketio.emit('lehrEINGABE',{'data': lehre, 'count': count},namespace='/synja_de', room = synja.id)
                  else: socketio.emit('lehrEINGABE',{'data': lehre, 'count': count},namespace='/synja_en', room = synja.id)
          #check if user has underlined text
          count += 1
        except:
          print("Synja error bt: "+synja.id)
          synja.running = False


          
      for l in lizas:
        if(not l.getUI().sendqueue.empty()):
          #print("sending something out")
          output = l.getUI().sendqueue.get()
          socketio.emit('my_response',{'data': output, 'count': count},namespace='/liza', room = l.id)
      
                   

@socketio.on('dialogeingabe', namespace='/synja_de')
def dialogeingabe_synja_de(message):
    dialogeingabe_synja(message)
    
@socketio.on('dialogeingabe', namespace='/synja_en')
def dialogeingabe_synja_en(message):
    dialogeingabe_synja(message)
  
def dialogeingabe_synja(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    zeitpunkt = datetime.datetime.now().strftime('%H:%M:%S')
    name = 'You'
    for synja in synjas:
        if synja.id == request.sid:
          if(synja.name != "NO_ACCOUNT"): name = synja.name
    emit('dialogEINGABE',{'data': '<b>'+str(name)+'</b>: \n'+str(message['data']), 'count': str(session['receive_count'])}) #TODO: vllt fehlerhaft
    #print("You: "+message['data'])
    #print("received \""  + message['data'] + "\" from " + request.sid)
    if (len(message['data']) > 0):
      for synja in synjas:
        if synja.id == request.sid:
          print("WA de: "+message['data']+" from ["+str(synja.name)+"]")
          synja.addDialogNutzer(message['data'])
          synja.input += 1
          print(synja.input)
          break
          
@socketio.on('lehreingabe', namespace='/synja_en')
def lehrausgabe_synja_en(message):
    lehrausgabe_synja(message)

@socketio.on('lehreingabe', namespace='/synja_de')
def lehrausgabe_synja_de(message):
    lehrausgabe_synja(message)   
    
def lehrausgabe_synja(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('dialogEINGABE',{'data': 'You: \"'+message['data'] + '\"', 'count': session['receive_count']})
    #print("received \""  + message['data'] + "\" from " + request.sid)
    if (len(message['data']) > 0):
      for synja in synjas:
        if synja.id == request.sid:
          synja.addLehreNutzer(message['data'])
          synja.input = True
    
@socketio.on('my_broadcast_event', namespace='/synja_en')
def broadcast_message_synja_en(message):
    broadcast_message_synja(message)
    
@socketio.on('my_broadcast_event', namespace='/synja_de')
def broadcast_message_synja_de(message):
    broadcast_message_synja(message)
  
def broadcast_message_synja(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)


@socketio.on('join', namespace='/synja_en')
def join_synja_en(message):
    join_synja(message)  
 
@socketio.on('join', namespace='/synja_de')
def join_synja_de(message):
    join_synja(message)     
  
def join_synja(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.on('leave', namespace='/synja_en')
def leave_synja_en(message):
    leave_synja(message)  
    
    
@socketio.on('leave', namespace='/synja_de')
def leave_synja_de(message):
    leave_synja(message)  
    
def leave_synja(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.on('close_room', namespace='/synja_de')
def close_synja_de(message):
    close_synja(message)
    
@socketio.on('close_room', namespace='/synja_en')
def close_synja_en(message):
    close_synja(message)
  
def close_synja(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.',
                         'count': session['receive_count']},
         room=message['room'])
    close_room(message['room'])


@socketio.on('my_room_event', namespace='/synja_de')
def send_room_message_synja_de(message):
    send_room_message_synja(message)

@socketio.on('my_room_event', namespace='/synja_en')
def send_room_message_synja_en(message):
    send_room_message_synja(message)
        
def send_room_message_synja(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         room=message['room'])


@socketio.on('disconnect_request', namespace='/synja_en')
def disconnect_request_synja_en():
    disconnect_request_synja()
    
@socketio.on('disconnect_request', namespace='/synja_de')
def disconnect_request_synja_de():
    disconnect_request_synja()
  
def disconnect_request_synja():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()

       
          
@socketio.on('btn_de', namespace='/synja_en')
def change_lang_de_synja():
  for synja in synjas:
    if synja.id == request.sid:
      #print("WA de: "+message['data']+" from ["+str(synja.name)+"]")
      #print("SPRACHE DEUTSCH")
      synja.sprache = "de"
  emit('redirect', {'url': url_for('render_indexSynja_DE')}) 
      
@socketio.on('btn_en', namespace='/synja_de')
def change_lang_en_synja():
  for synja in synjas:
    if synja.id == request.sid:
      #print("WA de: "+message['data']+" from ["+str(synja.name)+"]")
      synja.sprache = "en"
  #print(currentroute[request.environ['REMOTE_ADDR']])
  emit('redirect', {'url': url_for('render_indexSynja_EN')}) 
      
@socketio.on('connect', namespace='/synja_en')
def connect_synja_en():
    connect_synja("en")
  
@socketio.on('connect', namespace='/synja_de')
def connect_synja_de():
    connect_synja("de") 
  
def connect_synja(sprache):
    if(request.sid not in connections):
      connections.append(request.sid)
      #print("New connection: " + request.sid)
    
    name = "NO_ACCOUNT"
  
    #print("WA neuer Nutzer: "+str(name)+" "+request.environ['REMOTE_ADDR'])
    nr = len(synjas)+1    
    Synja_ = Synja(request.sid, nr, name)
    Synja_.lehrmanager.neuernutzer = True
    Synja_.sprache = sprache
    synjas.append(Synja_)
    Synja_.start()
    global thread
    with thread_lock:
      if thread is None:
        thread = socketio.start_background_task(target=background_threadSynjaLiza)
    #emit('my_response', {'data': 'Connected\n', 'count': 0})         
    print("synja "+str(nr)+" connected")    
    
@socketio.on('disconnect', namespace='/synja_de')
def disconnect_synja_de():
    disconnect_synja()
  
@socketio.on('disconnect', namespace='/synja_en')
def disconnect_synja_en():
    disconnect_synja()

def disconnect_synja(): 
    print('Client disconnected', request.sid)

    for synja in synjas:
      if synja.id == request.sid:
        print("set to stop")
        synja.running = False
        nr = synja.id
        
    #print("synja "+str(nr)+" disconnected") 
    #print(synja.id)   

@socketio.on('my_ping', namespace='/synja_de')
def ping_pong_synja_de():
    emit('my_pong')        


@socketio.on('my_ping', namespace='/synja_en')
def ping_pong_synja_en():
    emit('my_pong')       
   

              
'''      
LIZACODE
Hier sind die eventhandler fuer indexLiza.html. 
'''
      
        
@socketio.on('my_event', namespace='/liza')
def message_liza(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'You: \"'+message['data'] + '\"', 'count': session['receive_count']})
    print("received \""  + message['data'] + "\" from " + request.sid)
    print("BLA: "+str(request.environ['REMOTE_ADDR']))
    if (len(message['data']) > 0):
      for l in lizas:
        if l.id == request.sid:
          l.getUI().add(message['data'])
          l.getUI().input = True
    
@socketio.on('my_broadcast_event', namespace='/liza')
def broadcast_message_liza(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)


@socketio.on('join', namespace='/liza')
def join_liza(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.on('leave', namespace='/liza')
def leave_liza(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.on('close_room', namespace='/liza')
def close_liza(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.',
                         'count': session['receive_count']},
         room=message['room'])
    close_room(message['room'])


@socketio.on('my_room_event', namespace='/liza')
def send_room_message_liza(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         room=message['room'])


@socketio.on('disconnect_request', namespace='/liza')
def disconnect_request_liza():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()


@socketio.on('my_ping', namespace='/liza')
def ping_pong_liza():
    emit('my_pong')
    
@socketio.on('connect', namespace='/liza')
def connect_liza():
    if(request.sid not in connections):
      #print("New connection: " + request.sid)
      connections.append(request.sid)
  
    #print("Creating new Liza.")
    nr = len(lizas)+1    
    Liza = L(request.sid, nr)
    thread_list.append(Liza)
    lizas.append(Liza)
    Liza.start()
    global thread
    with thread_lock:
        if thread is None:
          thread = socketio.start_background_task(target=background_threadSynjaLiza)
    #emit('my_response', {'data': 'Connected\n', 'count': 0})         
     
    
@socketio.on('disconnect', namespace='/liza')
def disconnect_liza():
    print('Client disconnected', request.sid)
    for l in lizas:
      if l.id == request.sid:
        print("set to stop")
        l.running = False
        l.running = False
  
if __name__ == '__main__':
  #s = serve(app, host='127.0.0.1', port=80)
  socketio.run(app, host='0.0.0.0', port=80)
  #socketio.run(app, host='127.0.0.1', port=80)
 
