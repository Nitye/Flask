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
    console.log('check');
    socketio.emit('output'); 
  });
};

const loadOutput = (name) => {
  socketio.on('poker_output', function (data) {
    let out = ''; 
    if (name == data['name']) {
      out = data['command'];
    } else {
      out = data['alt_command'];
    }
    console.log(out);
    document.getElementById('poker_outputs').innerHTML += `[${data['code']}][${data['name']}]: ${out} <br>`;
  });
};

const recvMessage = () => {
  socketio.on('message', function (data) {
    document.getElementById('output').innerHTML += `<p>${data['name']+data['message']+data['room']}</p>`;
    let members = '';
    for ( let i = 0; i < data['number_of_members']; i++) {
      members += `<li>${data['member_list'][i]}</li>`
    };
    document.getElementById('members').innerHTML = `<ul>${members}</ul>`
  });
};

const serverStartGame = () => {
  socketio.on('server_start_game', function () {
    socketio.emit('start_game_server');
  });
};

const startGame = (name, code) => {
  socketio.on('start_game', function () {
    const url = `/game/${code}/${name}`;
    window.location.href = url;
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
