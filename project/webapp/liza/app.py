#!/usr/bin/env python
from threading import Lock
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from l import L



# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asde24oyx58ci6ad3skgr91ua2wp3oasd'
socketio = SocketIO(app, async_mode=async_mode)




thread = None
thread_lock = Lock()

thread_list = []
connections = []
lizas = []

def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
      count += 1
      #socketio.emit('my_response',
      #              {'data': 'Server generated event', 'count': count},
      #              namespace='/test', room = connections[0])
      socketio.sleep(0.1)
      for l in lizas:
        if(not l.getUI().sendqueue.empty()):
          #print("sending something out")
          output = l.getUI().sendqueue.get()
          socketio.emit('my_response',{'data': output, 'count': count},namespace='/test', room = l.id)

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('my_event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'You: \"'+message['data'] + '\"', 'count': session['receive_count']})
    print("received \""  + message['data'] + "\" from " + request.sid)
    if (len(message['data']) > 0):
      for l in lizas:
        if l.id == request.sid:
          l.getUI().add(message['data'])
          l.getUI().input = True
    
@socketio.on('my_broadcast_event', namespace='/test')
def test_broadcast_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)


@socketio.on('join', namespace='/test')
def join(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.on('leave', namespace='/test')
def leave(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.on('close_room', namespace='/test')
def close(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.',
                         'count': session['receive_count']},
         room=message['room'])
    close_room(message['room'])


@socketio.on('my_room_event', namespace='/test')
def send_room_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         room=message['room'])


@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()


@socketio.on('my_ping', namespace='/test')
def ping_pong():
    emit('my_pong')


@socketio.on('connect', namespace='/test')
def test_connect():
    
    print("New connection: " + request.sid)
    connections.append(request.sid)
    
    print("Creating new Liza.")
    nr = len(lizas)+1    
    Liza = L(request.sid, nr)
    thread_list.append(Liza)
    lizas.append(Liza)
    Liza.start()
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)
    #emit('my_response', {'data': 'Connected\n', 'count': 0})         
    
    

    
    
@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)
    for l in lizas:
      if l.id == request.sid:
        print("set to stop")
        l.running = False
        l.getUI().running = False
        
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port='80')