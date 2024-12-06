from flask import Flask, render_template_string, request, session, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room, send
import random
from data import chat_history, user_balances, research_papers, rules, functions, knowledge_areas

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management
socketio = SocketIO(app)

@app.route('/')
def home():
    return render_template_string('''
        <h1>Welcome</h1>
        <a href="{{ url_for('knowledge_base') }}">Knowledge Base</a><br>
        <a href="{{ url_for('explore_system') }}">Explore System</a><br>
        <a href="{{ url_for('learn_system') }}">Learn System</a><br>
        <a href="{{ url_for('exam_system') }}">Exam System</a><br>
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
    important_rules = rules.get(chosen_function, [])
    
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
        <p>Content for {{ chosen_function }}</p>
        <ul>
            {% for rule in important_rules %}
                <li>{{ rule }}</li>
            {% endfor %}
        </ul>
        <form method="post" action="/post_research">
            <input type="hidden" name="branch" value="{{ chosen_function }}">
            <button type="submit">Post Research</button>
        </form>
    ''', chosen_function=chosen_function, branches=branches, important_rules=important_rules)

@app.route('/branch', methods=['POST'])
def branch():
    chosen_branch = request.form['branch']
    important_rules = rules.get(chosen_branch, [])
    
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
        <ul>
            {% for rule in important_rules %}
                <li>{{ rule }}</li>
            {% endfor %}
        </ul>
        <form method="post" action="/post_research">
            <input type="hidden" name="branch" value="{{ chosen_branch }}">
            <button type="submit" class="subitem">Post Research</button>
        </form>
    ''', chosen_branch=chosen_branch, important_rules=important_rules)

@app.route('/post_research', methods=['POST'])
def post_research():
    branch = request.form['branch']
    return render_template_string('''
        <div style="text-align: right;">
            <a href="{{ url_for('home') }}">Home</a>
        </div>
        <h1>Post Research in {{ branch }}</h1>
        <form method="post" action="/publish_research">
            <input type="hidden" name="branch" value="{{ branch }}">
            <textarea name="research_content" rows="10" cols="50" placeholder="Write your research here..."></textarea><br>
            <button type="submit">Publish</button>
        </form>
    ''', branch=branch)

@app.route('/publish_research', methods=['POST'])
def publish_research():
    branch = request.form['branch']
    research_content = request.form['research_content']
    if branch not in research_papers:
        research_papers[branch] = []
    research_papers[branch].append(research_content)
    return render_template_string('''
        <div style="text-align: right;">
            <a href="{{ url_for('home') }}">Home</a>
        </div>
        <h1>Research Published in {{ branch }}</h1>
        <p>{{ research_content }}</p>
        <a href="{{ url_for('explore_system') }}">Explore System</a>
    ''', branch=branch, research_content=research_content)

@app.route('/explore_system')
def explore_system():
    return render_template_string('''
        <div style="text-align: right;">
            <a href="{{ url_for('home') }}">Home</a>
        </div>
        <h1>Explore System</h1>
        <ul>
            {% for main_area, branches in knowledge_areas.items() %}
                <li>
                    <h2><a href="{{ url_for('view_research', area=main_area) }}">{{ main_area }}</a></h2>
                    <ul>
                        {% for branch in branches %}
                            <li>
                                <h3><a href="{{ url_for('view_branch_research', branch=branch) }}">{{ branch }}</a></h3>
                            </li>
                        {% endfor %}
                    </ul>
                </li>
            {% endfor %}
        </ul>
    ''', knowledge_areas=knowledge_areas)

@app.route('/view_research/<area>')
def view_research(area):
    papers = research_papers.get(area, [])
    return render_template_string('''
        <div style="text-align: right;">
            <a href="{{ url_for('home') }}">Home</a>
        </div>
        <h1>Research in {{ area }}</h1>
        <ul>
            {% for paper in papers %}
                <li>{{ paper }}</li>
            {% endfor %}
        </ul>
        <a href="{{ url_for('explore_system') }}">Back to Explore System</a>
    ''', area=area, papers=papers)

@app.route('/view_branch_research/<branch>')
def view_branch_research(branch):
    papers = research_papers.get(branch, [])
    return render_template_string('''
        <div style="text-align: right;">
            <a href="{{ url_for('home') }}">Home</a>
        </div>
        <h1>Research in {{ branch }}</h1>
        <ul>
            {% for paper in papers %}
                <li>{{ paper }}</li>
            {% endfor %}
        </ul>
        <a href="{{ url_for('explore_system') }}">Back to Explore System</a>
    ''', branch=branch, papers=papers)

# Learn System Routes
@app.route('/learn_system', methods=['GET', 'POST'])
def learn_system():
    if request.method == 'POST':
        chosen_topic = request.form['topic']
        if chosen_topic in rules:
            rule = random.choice(rules[chosen_topic])
            return render_template_string('''
                <div style="text-align: right;">
                    <a href="{{ url_for('home') }}">Home</a>
                </div>
                <h1>Learn System</h1>
                <p>Topic: {{ chosen_topic }}</p>
                <p>Rule: {{ rule }}</p>
                <form method="post" action="/learn_system">
                    <input type="hidden" name="topic" value="{{ chosen_topic }}">
                    <button type="submit" name="action" value="master">Master</button>
                    <button type="submit" name="action" value="forget">Forget</button>
                </form>
            ''', chosen_topic=chosen_topic, rule=rule)
    return render_template_string('''
        <div style="text-align: right;">
            <a href="{{ url_for('home') }}">Home</a>
        </div>
        <h1>Learn System</h1>
        <form method="post" action="/learn_system">
            <label for="topic">Choose a topic:</label>
            <select id="topic" name="topic">
                {% for function, branches in knowledge_areas.items() %}
                    <option value="{{ function }}">{{ function }}</option>
                    {% for branch in branches %}
                        <option value="{{ branch }}">-- {{ branch }}</option>
                    {% endfor %}
                {% endfor %}
            </select>
            <button type="submit">Start Learning</button>
        </form>
    ''', knowledge_areas=knowledge_areas)

# Exam System Routes
@app.route('/exam_system', methods=['GET', 'POST'])
def exam_system():
    if request.method == 'POST':
        chosen_topic = request.form['topic']
        if chosen_topic in rules:
            questions = random.sample(rules[chosen_topic], min(5, len(rules[chosen_topic])))
            session['questions'] = questions
            session['current_question'] = 0
            session['score'] = 0
            return redirect(url_for('take_exam'))
    return render_template_string('''
        <div style="text-align: right;">
            <a href="{{ url_for('home') }}">Home</a>
        </div>
        <h1>Exam System</h1>
        <form method="post" action="/exam_system">
            <label for="topic">Choose a topic:</label>
            <select id="topic" name="topic">
                {% for function, branches in knowledge_areas.items() %}
                    <option value="{{ function }}">{{ function }}</option>
                    {% for branch in branches %}
                        <option value="{{ branch }}">-- {{ branch }}</option>
                    {% endfor %}
                {% endfor %}
            </select>
            <button type="submit">Start Exam</button>
        </form>
    ''', knowledge_areas=knowledge_areas)

@app.route('/take_exam', methods=['GET', 'POST'])
def take_exam():
    if request.method == 'POST':
        action = request.form['action']
        if action == 'correct':
            session['score'] += 20
        session['current_question'] += 1
        if session['current_question'] >= len(session['questions']):
            return redirect(url_for('exam_result'))
    current_question = session['questions'][session['current_question']]
    return render_template_string('''
        <div style="text-align: right;">
            <a href="{{ url_for('home') }}">Home</a>
        </div>
        <h1>Exam System</h1>
        <p>Question: {{ current_question }}</p>
        <form method="post" action="/take_exam">
            <button type="submit" name="action" value="correct">Correct</button>
            <button type="submit" name="action" value="incorrect">Incorrect</button>
        </form>
    ''', current_question=current_question)

@app.route('/exam_result')
def exam_result():
    score = session.get('score', 0)
    result = "Pass" if score >= 80 else "Fail"
    return render_template_string('''
        <div style="text-align: right;">
            <a href="{{ url_for('home') }}">Home</a>
        </div>
        <h1>Exam Result</h1>
        <p>Your score: {{ score }}</p>
        <p>Result: {{ result }}</p>
        <a href="{{ url_for('exam_system') }}">Back to Exam System</a>
    ''', score=score, result=result)

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