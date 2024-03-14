def player_input(queue, code, name, data):
  queue.put(code)
  queue.put(name)
  queue.put(data)