from flask import Flask, render_template_string, request, session, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room, send

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management
socketio = SocketIO(app)

# In-memory dictionary to store chat history and user balances
chat_history = {}
user_balances = {}

@app.route('/')
def home():
    return render_template_string('''
        <h1>Welcome</h1>
        <a href="{{ url_for('function1') }}">Social System</a><br>
        <a href="{{ url_for('function2') }}">Function 2</a>
    ''')

@app.route('/function1', methods=['GET', 'POST'])
def function1():
    if request.method == 'POST' and 'amount' in request.form:
        uid = request.form['uid']
        amount = float(request.form['amount'])
        user_balances[uid] = user_balances.get(uid, 0.0) + amount
        chat_history.setdefault(uid, []).append(f"${amount}")
        return render_template_string('''
            <h1>Chat with {{ uid }}</h1>
            <div id="chat">
                <ul id="messages">
                    {% for message in chat_history.get(uid, []) %}
                        <li>{{ message }}</li>
                    {% endfor %}
                </ul>
            </div>
            <label for="message">Message:</label>
            <input id="message" autocomplete="off"><button onclick="sendMessage()">Send</button>
            <form method="post" action="/function1">
                <input type="hidden" name="uid" value="{{ uid }}">
                <label for="amount">Amount:</label>
                <input type="number" id="amount" name="amount" required>
                <button type="submit">Pay</button>
            </form>
            <p>Payment Successful: You have sent ${{ amount }} to {{ uid }}.</p>
            <script src="//cdnjs.cloudflare.com/ajax/libs/socket.io/3.1.3/socket.io.min.js"></script>
            <script type="text/javascript" charset="utf-8">
                var socket = io();
                var uid = "{{ uid }}";
                socket.emit('join', uid);
                socket.on('message', function(msg){
                    var li = document.createElement("li");
                    li.appendChild(document.createTextNode(msg));
                    document.getElementById("messages").appendChild(li);
                });
                function sendMessage() {
                    var msg = document.getElementById("message").value;
                    socket.emit('message', {uid: uid, msg: msg});
                    document.getElementById("message").value = '';
                }
            </script>
            <a href="{{ url_for('function1') }}">Back</a>
        ''', uid=uid, chat_history=chat_history, amount=amount)
    elif request.method == 'POST' and 'uid' in request.form:
        uid = request.form['uid']
        return render_template_string('''
            <h1>Chat with {{ uid }}</h1>
            <div id="chat">
                <ul id="messages">
                    {% for message in chat_history.get(uid, []) %}
                        <li>{{ message }}</li>
                    {% endfor %}
                </ul>
            </div>
            <label for="message">Message:</label>
            <input id="message" autocomplete="off"><button onclick="sendMessage()">Send</button>
            <form method="post" action="/function1">
                <input type="hidden" name="uid" value="{{ uid }}">
                <label for="amount">Amount:</label>
                <input type="number" id="amount" name="amount" required>
                <button type="submit">Pay</button>
            </form>
            <script src="//cdnjs.cloudflare.com/ajax/libs/socket.io/3.1.3/socket.io.min.js"></script>
            <script type="text/javascript" charset="utf-8">
                var socket = io();
                var uid = "{{ uid }}";
                socket.emit('join', uid);
                socket.on('message', function(msg){
                    var li = document.createElement("li");
                    li.appendChild(document.createTextNode(msg));
                    document.getElementById("messages").appendChild(li);
                });
                function sendMessage() {
                    var msg = document.getElementById("message").value;
                    socket.emit('message', {uid: uid, msg: msg});
                    document.getElementById("message").value = '';
                }
            </script>
            <a href="{{ url_for('function1') }}">Back</a>
        ''', uid=uid, chat_history=chat_history)
    return render_template_string('''
        <h1>Social System</h1>
        <form method="post" action="/function1">
            <label for="uid">Enter UID:</label>
            <input type="text" id="uid" name="uid" required>
            <button type="submit">Start</button>
        </form>
        <a href="{{ url_for('home') }}">Back</a>
    ''')

@app.route('/function2')
def function2():
    return render_template_string('''
        <h1>Empty Function</h1>
        <p>This function is currently empty.</p>
        <a href="{{ url_for('home') }}">Back</a>
    ''')

@socketio.on('join')
def on_join(data):
    join_room(data)

@socketio.on('leave')
def on_leave(data):
    leave_room(data)

@socketio.on('message')
def handle_message(data):
    uid = data['uid']
    msg = data['msg']
    chat_history.setdefault(uid, []).append(msg)
    send(msg, to=uid)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5004, debug=True)