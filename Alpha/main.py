import website
from website import sockets,  functions
import poker
from threading import Thread
from queue import Queue 

app, db, socketio = website.create_app()

def main():
  socketio.run(app)

# def print_output():
#   s_to_c = website.s_to_c
#   c_to_s = sockets.c_to_s
#   while True:
#     code = c_to_s.get()
#     name = c_to_s.get()
#     hh = int(c_to_s.get())
#     if hh == 1:
#       print('test 1')
#       functions.player_input(s_to_c, code, name, 'check')
#     elif hh == 2:
#       print('Test 2')
#       functions.player_input(s_to_c, code, name, 'call')
#     elif hh == 3:
#       print('test 3')
#       functions.player_input(s_to_c, code, name, 'fold')
#     else:
#       print('nope')

t1 = Thread(target=main)
t2 = Thread(target=poker.play, args=(3, 1000, ['n','p','t'], website.s_to_c, website.c_to_s, socketio))
t1.start()
t2.start()