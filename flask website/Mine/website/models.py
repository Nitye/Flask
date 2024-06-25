from . import db
from flask_login import UserMixin
from queue import Queue

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key = True)
  email = db.Column(db.String(50), unique = True)
  password = db.Column(db.String(50))
  first_name = db.Column(db.String(30), unique = True)
  current_sid = db.Column(db.String(20), default = None)
  game = db.Column(db.Integer, db.ForeignKey('game.id'))
  room = db.Column(db.String(4), db.ForeignKey('my_room.id'))

class Game(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  number_of_players = db.Column(db.Integer)
  players = db.relationship('User')

class my_room(db.Model):
  id = db.Column(db.String(4), primary_key = True)
  number_of_members = db.Column(db.Integer)
  bank = db.Column(db.Integer)
  members = db.relationship('User')
  messages = db.relationship('Message')

  def __init__(self, id):
    self.id = id
    self.number_of_members = 0

class Message(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  message = db.Column(db.String(400))
  rendered = db.Column(db.Boolean, default = False)
  room = db.Column(db.String(4), db.ForeignKey('my_room.id'))

