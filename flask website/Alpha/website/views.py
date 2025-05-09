from flask import session, flash, Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from flask_socketio import emit
from . import db, s_to_c, c_to_s
from .models import User, my_room
from .sockets import socketio
from .poker import play
import random
from string import ascii_uppercase
from  threading import Thread
from queue import Queue

views = Blueprint('views', __name__)

def generate_unique_code(length):
  code = ''
  for _ in range(length):
    code += random.choice(ascii_uppercase)
  return code

@views.route('/')
def site_home():
  return render_template('site_home.html',  user = None)

@views.route('/<name>/home', methods = ['POST', 'GET'])
@login_required
def home(name):
  empty_rooms = my_room.query.filter(my_room.number_of_members <= 0).all()
  for i in empty_rooms:
    db.session.delete(i)
  db.session.commit()
  if request.method == 'POST':
    code = request.form.get('room_code')
    join = request.form.get('join', False)
    create = request.form.get('create', False)
    room = code
    check_code = my_room.query.filter_by(id = code).first()
    if not code and join != False:
      flash('Please enter a room code', category='error')
    if not check_code and join != False:
      flash('Room doesn\'t exist', category = 'error')
    if create != False:
      room = generate_unique_code(4)
      print(room)
      new_room = my_room(id = room)
      db.session.add(new_room)
      db.session.commit()
      return redirect(f'/room/{room}/{name}')
    if join != False and check_code:
      print(room)
      return redirect(f'/room/{room}/{name}')
  return render_template('home.html',  user = User.query.filter_by(first_name = name).first())

@views.route('/room/<code>/<name>', methods = ['POST','GET'])
@login_required
def room(code, name):
  check_code = my_room.query.filter_by(id = code).first()
  old_messages = []
  members = [name]
  if not check_code:
    return redirect(f'/{name}/home')
  else:
    for i in check_code.messages:
      old_messages.append(i.message)
    for j in check_code.members:
      if j.first_name not in members:
        members.append(j.first_name) 
  if request.method == 'POST':
    start = request.form.get('start')
    bank = request.form.get('bank')
    check_code.bank = bank
    db.session.commit()
    if start != False:
      if len(members) < 2:
        flash('Not enough members', category='error')
      else:
        socketio.emit('server_start_game', code)
        t = Thread(target=play, args=(len(members), bank, members, s_to_c, c_to_s, socketio, code))
        t.start()
        print(members)
        return redirect(f'/game/{code}/{name}')
  return render_template('room.html', user = User.query.filter_by(first_name = name).first(), code = code, old_messages = old_messages, members=set(members), poker = False)

@views.route('/game/<code>/<name>', methods = ['POST','GET'])
@login_required
def game_page(code, name):
  check_code = my_room.query.filter_by(id = code).first()
  old_messages = []
  members = [name]
  bank = check_code.bank
  if not check_code:
    return redirect(f'/{name}/home')
  else:
    for i in check_code.messages:
      old_messages.append(i.message)
    for j in check_code.members:
      if j.first_name not in members:
        members.append(j.first_name)
  return render_template('game.html', user = User.query.filter_by(first_name = name).first(), code = code, old_messages = old_messages, members=set(members))

@views.route('/db')
@login_required
def check_db():
  room_entries = my_room.query.all()
  user_entries = User.query.all()
  empty_room_entries = my_room.query.filter(my_room.number_of_members <= 1).all()
  return render_template('db.html', empty_rooms = empty_room_entries, rooms = room_entries, users = user_entries, user = current_user)
