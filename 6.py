from flask import Flask, render_template_string, request, session, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room, send

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management
socketio = SocketIO(app)

# In-memory dictionary to store chat history and user balances
chat_history = {}
user_balances = {}

functions = [
    "Art",
    "Computer Science",
    "Economics",
    "English",
    "Geography",
    "History",
    "Math",
    "Music",
    "Physical Education",
    "Science"
]

knowledge_areas = {
    "Art": [
        "Painting",
        "Sculpture",
        "Photography",
        "Drawing",
        "Printmaking",
        "Ceramics",
        "Textiles",
        "Digital Art",
        "Art History",
        "Graphic Design"
    ],
    "Computer Science": [
        "Algorithms",
        "Data Structures",
        "Operating Systems",
        "Databases",
        "Networking",
        "Artificial Intelligence",
        "Machine Learning",
        "Cybersecurity",
        "Software Engineering",
        "Web Development"
    ],
    "Economics": [
        "Microeconomics",
        "Macroeconomics",
        "International Economics",
        "Development Economics",
        "Labor Economics",
        "Public Economics",
        "Health Economics",
        "Environmental Economics",
        "Behavioral Economics",
        "Econometrics"
    ],
    "English": [
        "Literature",
        "Creative Writing",
        "Linguistics",
        "Grammar",
        "Composition",
        "Rhetoric",
        "Poetry",
        "Drama",
        "Prose",
        "Literary Theory"
    ],
    "Geography": [
        "Physical Geography",
        "Human Geography",
        "Cartography",
        "Geographic Information Systems",
        "Urban Geography",
        "Environmental Geography",
        "Economic Geography",
        "Political Geography",
        "Cultural Geography",
        "Historical Geography"
    ],
    "History": [
        "Ancient History",
        "Medieval History",
        "Modern History",
        "World History",
        "Military History",
        "Social History",
        "Economic History",
        "Cultural History",
        "Political History",
        "Historiography"
    ],
    "Math": [
        "Algebra",
        "Geometry",
        "Calculus",
        "Statistics",
        "Trigonometry",
        "Number Theory",
        "Combinatorics",
        "Probability",
        "Linear Algebra",
        "Differential Equations"
    ],
    "Music": [
        "Music Theory",
        "Composition",
        "Music History",
        "Performance",
        "Conducting",
        "Music Technology",
        "Ethnomusicology",
        "Jazz Studies",
        "Music Education",
        "Music Therapy"
    ],
    "Physical Education": [
        "Exercise Physiology",
        "Kinesiology",
        "Sports Psychology",
        "Motor Learning",
        "Biomechanics",
        "Sports Nutrition",
        "Adapted Physical Education",
        "Health Education",
        "Sports Management",
        "Coaching"
    ],
    "Science": [
        "Physics",
        "Chemistry",
        "Biology",
        "Earth Science",
        "Astronomy",
        "Environmental Science",
        "Materials Science",
        "Genetics",
        "Ecology",
        "Geology"
    ]
}

@app.route('/')
def home():
    return render_template_string('''
        <h1>Welcome</h1>
        <a href="{{ url_for('knowledge_base') }}">Knowledge Base</a><br>
        <a href="{{ url_for('function1') }}">Social System</a><br>
        <a href="{{ url_for('function2') }}">Empty Function</a>
    ''')

# Knowledge Base Routes
@app.route('/knowledge_base', methods=['GET'])
def knowledge_base():
    session['history'] = []  # Initialize history in session
    return render_template_string('''
        <div style="text-align: right;">
            <a href="{{ url_for('home') }}">Home</a>
        </div>
        <h1>Knowledge Base</h1>
        <form method="post" action="/choose">
            {% for function in functions %}
                <button type="submit" name="function" value="{{ function }}">{{ function }}</button>
            {% endfor %}
        </form>
    ''', functions=functions)

@app.route('/choose', methods=['POST'])
def choose():
    chosen_function = request.form['function']
    branches = knowledge_areas.get(chosen_function, ["No branches available."])
    
    if 'history' not in session:
        session['history'] = []
    session['history'].append(('choose', chosen_function))
    session.modified = True

    return render_template_string('''
        <div style="text-align: right;">
            <a href="{{ url_for('home') }}">Home</a>
        </div>
        <h1>{{ chosen_function }}</h1>
        <form method="post" action="/branch">
            {% for branch in branches %}
                <button type="submit" name="branch" value="{{ branch }}">{{ branch }}</button>
            {% endfor %}
        </form>
    ''', chosen_function=chosen_function, branches=branches)

@app.route('/branch', methods=['POST'])
def branch():
    chosen_branch = request.form['branch']
    
    if 'history' not in session:
        session['history'] = []
    session['history'].append(('branch', chosen_branch))
    session.modified = True

    return render_template_string('''
        <div style="text-align: right;">
            <a href="{{ url_for('home') }}">Home</a>
        </div>
        <h1>{{ chosen_branch }}</h1>
        <p>Content for {{ chosen_branch }}</p>
    ''', chosen_branch=chosen_branch)

# Social System Routes
@app.route('/function1', methods=['GET', 'POST'])
def function1():
    if request.method == 'POST' and 'amount' in request.form:
        uid = request.form['uid']
        amount = float(request.form['amount'])
        user_balances[uid] = user_balances.get(uid, 0.0) + amount
        chat_history.setdefault(uid, []).append(f"${amount}")
        return render_template_string('''
            <div style="text-align: right;">
                <a href="{{ url_for('home') }}">Home</a>
            </div>
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
        ''', uid=uid, chat_history=chat_history, amount=amount)
    elif request.method == 'POST' and 'uid' in request.form:
        uid = request.form['uid']
        return render_template_string('''
            <div style="text-align: right;">
                <a href="{{ url_for('home') }}">Home</a>
            </div>
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
        ''', uid=uid, chat_history=chat_history)
    return render_template_string('''
        <div style="text-align: right;">
            <a href="{{ url_for('home') }}">Home</a>
        </div>
        <h1>Social System</h1>
        <form method="post" action="/function1">
            <label for="uid">Enter UID:</label>
            <input type="text" id="uid" name="uid" required>
            <button type="submit">Start</button>
        </form>
    ''')

@app.route('/function2', methods=['GET'])
def function2():
    return render_template_string('''
        <div style="text-align: right;">
            <a href="{{ url_for('home') }}">Home</a>
        </div>
        <h1>Empty Function</h1>
        <p>This function is currently empty.</p>
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
    socketio.run(app, host='0.0.0.0', port=5008, debug=True)