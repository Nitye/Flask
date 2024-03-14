from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from queue import Queue

db = SQLAlchemy()
DB_NAME = 'my_database6.db'
s_to_c = Queue()
c_to_s = Queue()

def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = 'iabtvcaaabucbau'
  app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
  db.init_app(app)
  from .views import views
  from .auth import auth
  from .models import User, my_room
  from .sockets import socketio
  socketio.init_app(app)
  app.register_blueprint(views, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/')
  app.app_context().push()
  db.create_all()
  login_manager = LoginManager()
  login_manager.login_view = 'auth.login'
  login_manager.init_app(app)
  @login_manager.user_loader
  def load_user(id):
    return User.query.get(int(id))
  return app, db, socketio
