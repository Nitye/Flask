var socketio = io({autoConnect : false});

const testFunc = () => {
  socketio.emit('received_message');
  socketio.emit('blah', 'Test');
  socketio.on('test', function (data) {
    console.log(data);
  });
};

const loadMessages = () => {
  socketio.on('load_messages', function (data) {
    document.getElementById('output').innerHTML += data;
    document.getElementById('Message').value = null;
  });
};

const recvOutput = () => {
  socketio.on('sending_output', function () {
    socketio.emit('output');
  });
};

const loadOutput = () => {
  socketio.on('poker_output', function (data) {
    document.getElementById('poker_outputs').innerHTML += `[${data['code']}][${data['name']}]: ${data['command']} <br>`;
  });
};

const recvMessage = () => {
  socketio.on('message', function (data) {
    document.getElementById('output').innerHTML += `<p>${data['name']+data['message']+data['room']}</p>`;
    let members = '';
    for ( let i = 0; i < data['number_of_members']; i++) {
      members += `<li>${data['member_list'][i]}</li>`
    };
    console.log(members);
    document.getElementById('members').innerHTML = `<ul>${members}</ul>`
  });
};

const sendMessage = (name) => {
  const msg = document.getElementById('Message').value
  socketio.emit('message_sent', {'name': name, 'msg': msg})
  document.getElementById('Message').value = null;
};

const connect_to_room = (name, code) => {
  socketio.connect();
  socketio.emit('join_room', name, code);
}

const disconnect_to_room = (name, code) => {
  socketio.emit('leave_room', name, code);
};
