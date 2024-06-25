def player_input(queue, code, name, data):
  queue.put(code)
  queue.put(name)
  queue.put(data)

def player_output(queue, code, socketio, name, data, alt_data):
  queue.put(code)
  queue.put(name)
  queue.put(data)
  queue.put(alt_data)
  socketio.emit('sending_output')
  print('sending output',  code, name, data, alt_data)

def take_input(queue, socketio):
  socketio.emit('send_input')
  queue.get()
  queue.get()
  inp = queue.get()
  return inp