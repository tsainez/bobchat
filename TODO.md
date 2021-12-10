# 📝 TODO

## Using Bootstrap for front-end rendering

We should probably make our front-end rendering look significantly nicer by using [Flask-Bootstrap](https://pythonhosted.org/Flask-Bootstrap/).

- Might want to model after the [example project](https://github.com/mbr/flask-bootstrap/tree/master/sample_app) posted on GitHub.
  - This example appears to be using the **application factory** (`__init__.py`) pattern as well, so it should just fit easily.

---

## Website Hosting

We need to host our website.

Our options in order of preference:

- Host on cloud.google.com (**most preferred**)

  - More effort to get started
  - Can do anything
  - Free option is limited to trial period]

- Host on PythonAnywhere.com

  - If cloud.google.com is too much work, we can resort to this... (for quick and easy hosting)
  - Very easy, but limited features
  - Incudes free forever option
  - [Beginners guide](https://blog.pythonanywhere.com/121/)

- Host on Heroku.com
  - If unable to host on PythonAnywhere.com, then this is probably our last resort
  - Easy to get started
  - More advanced features (than PythonAnywhere.com)
  - Incudes free forever option

### Flask-SocketIO on backend:

- Provides access to low-latency two-way client-server communication for Python Flask apps
- `pip install flask_socketio`

From lecture slides:

```Python
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def connect():
    emit('connect', {'data':'Connected'})

if __name__ == '__main__':
    socketio.run(app)
```

### Socket.IO JS library on front end:

We probably want to add this to `base.html` in the templates folder, assuming that every other HTML file in template pulls from that.

In the `<head>` tag, we can add...

_HTML_

```HTML
<head>
    <script src="https://code.jquery.com/jquery-3.3.1.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.3.0/socket.io.js"></script>
    <script type="text/javascript">
        const socket = io("ws://localhost:5000");
        socket.on("connect", function(msg) {
            if(msg != undefined) {
                $('#log').append('<br>' + $('<div/>').text('Received: ' + msg.data).html());
            }
        });
    </script>
</head>
```

### Flask-SocketIO Echo (Send/Receive):

This is for testing and verifying purposes...

_JavaScript_

```JavaScript
// send
function echo(){
    socket.emit("echo", $('#msg').val());
}

// receive
socket.on("echo", msg => {
    $('#log').append('<br>' + $('<div/>').text('Received: ' + msg).html());
});
```

_HTML_

```HTML
<body>
    <h2>SocketIO Example</h2>
    <button onClick="echo()">Echo</button>
    <input type="text" id="msg">
    <div id="log"></div>
</body>
```

_Python_

```Python
# This receives a message sent with ‘echo’ and sends a message with ‘echo’
@socketio.on('echo')
def echo(message):
    print("received", message)
    emit('echo', message)
```

### Resources:

- https://socket.io/docs/v4
- https://flask-socketio.readthedocs.io/en/latest/
