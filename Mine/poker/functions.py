def player_input(queue, code, name, data):
  queue.put(code)
  queue.put(name)
  queue.put(data)

def player_output(queue, code, socketio, name, data):
  socketio.emit('sending_output')
  queue.put(code)
  queue.put(name)
  queue.put(data)

def take_input(queue, socketio):
  socketio.emit('send_input')
  queue.get()
  queue.get()
  inp = queue.get()
  return inp