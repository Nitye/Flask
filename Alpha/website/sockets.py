from flask import session, flash, Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from flask_socketio import join_room, leave_room, send, SocketIO
from . import db, s_to_c, c_to_s
from .models import User, my_room, Message
from .auth import auth as auth_bp
from .functions import player_input

socketio = SocketIO()

@socketio.on('connect')
def connect():
  print('Client Connected')

@socketio.on('disconnect')
def disconnect():
  print('Client has disconnected')

@socketio.on('blah')
def blah(data):
  socketio.emit('test', 'yeah')
  print(data)

@socketio.on('join_room')
def join__room(name, code):
  join_room(code)
  user = User.query.filter_by(first_name = name).first()
  user.room = code
  user.current_sid = request.sid
  room = my_room.query.get(code)
  num = 0
  members = User.query.filter_by(room = code).all()
  member_list = []
  for i in members:
    num += 1
    member_list.append(i.first_name)
  room.number_of_members = num
  db.session.commit()
  send({'name': name+':', 'message': " has entered the room ", 'room':code, 'member_list':member_list, 'number_of_members': room.number_of_members}, to=code)
  print(f'{name} has joined room {code}')

@socketio.on('leave_room')
def leave__room(name, code):
  user = User.query.filter_by(first_name = name).first()
  user.room = None
  member_list = []
  user.current_sid = None
  room = my_room.query.get(code)
  room.number_of_members -= 1
  for j in room.members:
      member_list.append(j.first_name)
  db.session.commit()
  leave_room(code)
  send({'name': name+':', 'message': " has left the room ", 'room':code, 'member_list':member_list, 'number_of_members':room.number_of_members}, to=code)
  print(f'{name} has left room {code}')

@socketio.on('message_sent')
def message_sent(data):
  name = data['name']
  user = User.query.filter_by(first_name = name).first()
  code = user.room
  new_message = Message(message = name+': '+data['msg'], room = code)
  db.session.add(new_message)
  db.session.commit()

@socketio.on('refresh_messages')
def refresh_messages(code):
  room = my_room.query.get(code)
  messages = ''
  for i in room.messages:
    if i.rendered:
      pass
    else:
      messages += '<p>'+i.message+'</p>'
      i.rendered = True
  db.session.commit()
  socketio.emit('load_messages', messages)

@socketio.on('set_1')
def set_1(name, code):
  player_input(c_to_s, code, name, '1')

@socketio.on('set_2')
def set_2(name, code):
  player_input(c_to_s, code, name, '2')

@socketio.on('set_3')
def set_3(name, code):
  player_input(c_to_s, code, name, '3')

@socketio.on('output')
def output():
  code = s_to_c.get()
  name = s_to_c.get()
  command = s_to_c.get()
  socketio.emit('poker_output', {'name':name, 'code': code, 'command': command})