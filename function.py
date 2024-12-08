from flask import Flask, render_template_string, request, session, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room, send
import random

notes = {}
chat_history = {}


user_balances = {}
payment_history = {}

rules = {
    "Computer Science": [
        "Operating systems manage hardware resources and provide a platform for running applications and services.",
        "Data structures organize and store data efficiently for quick access and modification.",
        "Algorithms are step-by-step procedures for solving problems and performing tasks.",
        "Networking involves connecting computers and devices to share data and resources.",
        "Databases store, retrieve, and manage data in a structured way.",
        "Cybersecurity protects systems, networks, and data from digital attacks.",
        "Software engineering applies engineering principles to software development.",
        "Artificial intelligence enables machines to perform tasks that typically require human intelligence.",
        "Machine learning is a subset of AI that allows systems to learn from data and improve over time.",
        "Web development involves creating websites and web applications using various technologies."
    ],
    "Algorithms": [
        "Algorithms should have a defined input and output.",
        "Every algorithm must terminate after a finite number of steps.",
        "Time complexity measures how execution time grows with input size.",
        "Space complexity evaluates the memory used by an algorithm.",
        "Divide-and-conquer splits problems into smaller subproblems for easier solving.",
        "Greedy algorithms optimize step-by-step without backtracking.",
        "Dynamic programming solves overlapping subproblems efficiently.",
        "Backtracking explores all possible solutions to find the best fit.",
        "Recursion requires a base case to terminate properly.",
        "Algorithmic stability ensures consistent output with varying input conditions."
    ],
    "Operating Systems": [
        "Operating systems manage communication between hardware and software.",
        "Multitasking enables running multiple processes simultaneously.",
        "Process synchronization ensures coordinated access to shared resources.",
        "Deadlock prevention and detection are vital for process management.",
        "Virtual memory allows systems to execute large programs beyond physical RAM.",
        "Scheduling algorithms optimize CPU time allocation to processes.",
        "File systems store, retrieve, and organize data on storage devices.",
        "Interrupts allow devices to signal the processor for immediate attention.",
        "User and kernel modes protect the operating system from unintended interference.",
        "Security features safeguard against unauthorized access and malicious attacks."
    ],

    "Science": [
        "The scientific method involves observation, hypothesis, experimentation, and conclusion.",
        "Matter is anything that has mass and takes up space.",
        "Energy is the ability to do work or cause change.",
        "The laws of thermodynamics govern the principles of energy transfer.",
        "Atoms are the basic units of matter.",
        "Chemical reactions involve the rearrangement of atoms to form new substances.",
        "Cells are the basic units of life.",
        "Evolution explains the diversity of life on Earth.",
        "The universe is expanding, as evidenced by the redshift of distant galaxies.",
        "The Earth's climate is influenced by both natural and human factors."
    ],
    "Physics": [
        "Newton's laws of motion describe the relationship between the motion of an object and the forces acting on it.",
        "The law of universal gravitation states that every mass attracts every other mass.",
        "Energy can neither be created nor destroyed, only transformed (conservation of energy).",
        "The speed of light in a vacuum is a universal constant.",
        "Quantum mechanics describes the behavior of particles on a very small scale.",
        "Relativity theory explains the relationship between space and time.",
        "Electromagnetism describes the interaction between electric charges and magnetic fields.",
        "Thermodynamics deals with heat, work, and temperature, and their relation to energy and physical properties.",
        "Wave-particle duality states that particles can exhibit both wave-like and particle-like properties.",
        "The standard model of particle physics describes the fundamental particles and their interactions."
    ],
    "Chemistry": [
        "The periodic table organizes elements by increasing atomic number and similar chemical properties.",
        "Chemical bonds form when atoms share or transfer electrons.",
        "Acids and bases react to form water and salts.",
        "The pH scale measures the acidity or basicity of a solution.",
        "Chemical kinetics studies the rates of chemical reactions.",
        "Thermochemistry involves the study of energy changes during chemical reactions.",
        "Organic chemistry focuses on compounds containing carbon.",
        "Inorganic chemistry deals with compounds that are not organic.",
        "Electrochemistry studies the relationship between electricity and chemical reactions.",
        "Stoichiometry involves the calculation of reactants and products in chemical reactions."
    ],
    "Biology": [
        "The cell theory states that all living organisms are composed of cells.",
        "DNA carries genetic information and is the blueprint for life.",
        "Photosynthesis converts light energy into chemical energy in plants.",
        "Cellular respiration converts glucose into usable energy (ATP) in cells.",
        "Genetics is the study of heredity and variation in organisms.",
        "Evolution by natural selection explains the adaptation of species over time.",
        "Ecosystems consist of interacting organisms and their physical environment.",
        "Homeostasis is the maintenance of a stable internal environment in an organism.",
        "Proteins are essential molecules that perform a variety of functions in cells.",
        "The immune system protects the body from pathogens and foreign substances."
    ]
}


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

app = Flask(__name__)
app.secret_key = 'your_secret_key'
socketio = SocketIO(app)

@app.route('/')
def home():
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Home</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background: linear-gradient(135deg, #74ebd5, #ACB6E5);
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }
                .container {
                    text-align: center;
                    background: white;
                    padding: 30px 20px;
                    border-radius: 15px;
                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
                    max-width: 400px;
                    width: 90%;
                }
                h1 {
                    color: #333;
                    font-size: 28px;
                    margin-bottom: 20px;
                }
                a {
                    display: block;
                    margin: 10px 0;
                    padding: 12px;
                    font-size: 16px;
                    font-weight: bold;
                    text-decoration: none;
                    color: white;
                    background-color: #007BFF;
                    border-radius: 8px;
                    transition: background-color 0.3s ease, transform 0.2s ease;
                }
                a:hover {
                    background-color: #0056b3;
                    transform: scale(1.05);
                }
                @media (max-width: 600px) {
                    h1 {
                        font-size: 24px;
                    }
                    a {
                        font-size: 14px;
                        padding: 10px;
                    }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Learn with friends!</h1>
                <a href="{{ url_for('knowledge_base') }}">Read System</a>
                <a href="{{ url_for('note_system') }}">Note System</a>
                <a href="{{ url_for('study_system') }}">Study System</a>
                <a href="{{ url_for('exam_system') }}">Exam System</a>
                <a href="{{ url_for('social_chat') }}">Chat System</a>
                <a href="{{ url_for('social_pay') }}">Pay System</a>
            </div>
        </body>
        </html>
    ''')

@app.route('/knowledge_base', methods=['GET'])
def knowledge_base():
    session['history'] = []
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Read System</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background: linear-gradient(135deg, #74ebd5, #ACB6E5);
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }
                .container {
                    width: 95%; /* Increased width for more space */
                    max-width: 1400px; /* Adjusted max width for larger screens */
                    background: white;
                    padding: 40px; /* Added padding for spaciousness */
                    border-radius: 15px;
                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
                    text-align: center;
                    overflow-y: auto;
                    max-height: 90vh;
                }
                h1 {
                    color: #333;
                    font-size: 32px;
                    margin-bottom: 30px;
                }
                .grid-layout {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); /* Flexible column sizing */
                    gap: 20px; /* Spacing between buttons */
                    justify-items: center;
                    margin-top: 20px;
                }
                button {
                    width: 180px; /* Standard button size */
                    height: 60px;
                    font-size: 16px;
                    border: none;
                    border-radius: 10px;
                    background-color: #007BFF;
                    color: white;
                    cursor: pointer;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                    transition: background-color 0.3s ease, transform 0.2s ease;
                }
                button:hover {
                    background-color: #0056b3;
                    transform: scale(1.05);
                }
                @media (max-width: 600px) {
                    button {
                        width: 140px; /* Smaller button size on mobile */
                        height: 50px;
                        font-size: 14px;
                    }
                }
                .back-button {
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    text-decoration: none;
                    background-color: #88d498;
                    color: white;
                    padding: 12px 24px;
                    border-radius: 20px;
                    font-size: 16px;
                    font-weight: bold;
                    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
                    transition: background-color 0.3s, transform 0.2s;
                }
                .back-button:hover {
                    transform: scale(1.05);
                    background-color: #66c282;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div style="position: fixed; top: 20px; right: 20px;">
                    <a href="{{ url_for('home') }}" class="back-button">Home</a>
                </div>
                <h1>Read System</h1>
                <div class="grid-layout">
                    {% for function in functions %}
                        <form method="post" action="/choose">
                            <button type="submit" name="function" value="{{ function }}">{{ function }}</button>
                        </form>
                    {% endfor %}
                </div>
            </div>
        </body>
        </html>
    ''', functions=functions)

@app.route('/choose', methods=['POST'])
def choose():
    chosen_function = request.form['function']
    branches = knowledge_areas.get(chosen_function, ["No branches available."])
    important_rules = rules.get(chosen_function, [])
    session['history'] = session.get('history', []) + [('choose', chosen_function)]
    session.modified = True
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{{ chosen_function }}</title>
            <style>
                body {
                    margin: 0;
                    padding: 0;
                    font-family: Arial, sans-serif;
                    background: linear-gradient(135deg, #74ebd5, #ACB6E5);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }
                .container {
                    width: 90%;
                    max-width: 1200px;
                    background: white;
                    padding: 30px;
                    border-radius: 15px;
                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
                    text-align: center;
                    overflow-y: auto;
                    max-height: 90vh;
                }
                h1 {
                    color: #333;
                    font-size: 28px;
                    margin-bottom: 20px;
                }
                .grid-layout {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                    gap: 15px;
                    justify-items: center;
                }
                button {
                    width: 150px; /* Fixed width */
                    height: 50px; /* Fixed height */
                    font-size: 16px; /* Font size */
                    border: none;
                    border-radius: 8px;
                    background-color: #007BFF;
                    color: white;
                    cursor: pointer;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Subtle shadow */
                    transition: background-color 0.3s ease, transform 0.2s ease;
                }
                button:hover {
                    background-color: #0056b3;
                    transform: scale(1.05);
                }
                @media (max-width: 600px) {
                    button {
                        width: 120px; /* Adjust for smaller screens */
                        height: 40px;
                        font-size: 14px;
                    }
                }
                .content-block {
                    text-align: left;
                    margin: 20px auto;
                    padding: 15px;
                    border-radius: 10px;
                    background: #f9f9f9;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                    color: #555;
                    font-size: 16px;
                    line-height: 1.6;
                }
                .back-button {
                    position: fixed;
                    top: 20px;
                    left: 20px;
                    text-decoration: none;
                    background-color: #88d498;
                    color: white;
                    padding: 12px 24px;
                    border-radius: 20px;
                    font-size: 16px;
                    font-weight: bold;
                    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
                    transition: background-color 0.3s, transform 0.2s;
                }
                .back-button:hover {
                    transform: scale(1.05);
                    background-color: #66c282;
                }
            </style>
        </head>
        <body>
            <a href="{{ url_for('knowledge_base') }}" class="back-button">Back</a>
            <div class="container">
                <h1>{{ chosen_function }}</h1>
                <div class="grid-layout">
                    {% for branch in branches %}
                        <form method="post" action="/branch" style="display: inline;">
                            <button type="submit" name="branch" value="{{ branch }}">{{ branch }}</button>
                        </form>
                    {% endfor %}
                </div>
                <div class="content-block">
                    <p><strong>Content for {{ chosen_function }}</strong></p>
                    <ul>
                        {% for rule in important_rules %}
                            <li>{{ rule }}</li>
                        {% endfor %}
                    </ul>
                </div>
            </div>
        </body>
        </html>
    ''', chosen_function=chosen_function, branches=branches, important_rules=important_rules)

@app.route('/branch', methods=['POST'])
def branch():
    chosen_branch = request.form['branch']
    important_rules = rules.get(chosen_branch, [])
    session['history'] = session.get('history', []) + [('branch', chosen_branch)]
    session.modified = True
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{{ chosen_branch }}</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background: linear-gradient(135deg, #74ebd5, #ACB6E5);
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: flex-start;
                    min-height: 100vh;
                }
                .container {
                    margin-top: 50px;
                    text-align: center;
                    background: white;
                    padding: 30px 20px;
                    border-radius: 15px;
                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
                    max-width: 600px;
                    width: 90%;
                }
                h1 {
                    color: #333;
                    font-size: 28px;
                    margin-bottom: 20px;
                }
                ul {
                    text-align: left;
                    list-style-type: disc;
                    margin: 20px auto;
                    padding: 0 20px;
                    color: #555;
                }
                li {
                    font-size: 16px;
                    margin-bottom: 10px;
                }
                a {
                    display: block;
                    margin: 10px auto;
                    padding: 12px;
                    font-size: 16px;
                    font-weight: bold;
                    text-decoration: none;
                    color: white;
                    background-color: #007BFF;
                    border-radius: 8px;
                    width: fit-content;
                    transition: background-color 0.3s ease, transform 0.2s ease;
                }
                a:hover {
                    background-color: #0056b3;
                    transform: scale(1.05);
                }
                .back-button {
                    position: fixed;
                    top: 20px;
                    left: 20px;
                    text-decoration: none;
                    background-color: #88d498;
                    color: white;
                    padding: 12px 24px;
                    border-radius: 20px;
                    font-size: 16px;
                    font-weight: bold;
                    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
                    transition: background-color 0.3s, transform 0.2s;
                }
                .back-button:hover {
                    transform: scale(1.05);
                    background-color: #66c282;
                }
            </style>
        </head>
        <body>
            <a href="javascript:history.back()" class="back-button">Back</a>
            <div class="container">
                <h1>{{ chosen_branch }}</h1>
                <ul>
                    {% for rule in important_rules %}
                        <li>{{ rule }}</li>
                    {% endfor %}
                </ul>
                <a href="{{ url_for('knowledge_base') }}">Back to Knowledge Base</a>
            </div>
        </body>
        </html>
    ''', chosen_branch=chosen_branch, important_rules=important_rules)

@app.route('/post_note', methods=['POST'])
def post_note():
    branch = request.form['branch']
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Take Note</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f9f9f9;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }
                .container {
                    background: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                    text-align: center;
                    max-width: 500px;
                    width: 90%;
                }
                h1 {
                    color: #333;
                    font-size: 24px;
                }
                textarea {
                    width: 100%;
                    padding: 10px;
                    margin-top: 10px;
                    font-size: 16px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                }
                button {
                    margin-top: 10px;
                    padding: 10px 20px;
                    font-size: 16px;
                    border: none;
                    border-radius: 5px;
                    background-color: #007BFF;
                    color: white;
                    cursor: pointer;
                    transition: background-color 0.3s;
                }
                button:hover {
                    background-color: #0056b3;
                }
                a {
                    text-decoration: none;
                    color: #007BFF;
                    margin-top: 10px;
                    display: inline-block;
                }
                a:hover {
                    text-decoration: underline;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div style="position: fixed; top: 20px; right: 20px;">
                    <a href="{{ url_for('home') }}" 
                    style="text-decoration: none; 
                            background-color: #88d498; 
                            color: white; 
                            padding: 12px 24px; 
                            border-radius: 20px; 
                            font-size: 16px; 
                            font-weight: bold; 
                            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15); 
                            transition: background-color 0.3s, transform 0.2s;">
                        Home
                    </a>
                </div>
                <h1>Take Note in {{ branch }}</h1>
                <form method="post" action="/publish_note">
                    <input type="hidden" name="branch" value="{{ branch }}">
                    <textarea name="note_content" rows="10" placeholder="Write your note here..."></textarea><br>
                    <button type="submit">Publish</button>
                </form>
            </div>
        </body>
        </html>
    ''', branch=branch)

@app.route('/publish_note', methods=['POST'])
def publish_note():
    branch = request.form['branch']
    note_content = request.form['note_content']
    notes.setdefault(branch, []).append(note_content)
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Note Published</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f9f9f9;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }
                .container {
                    background: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                    text-align: center;
                    max-width: 500px;
                    width: 90%;
                }
                h1 {
                    color: #333;
                    font-size: 24px;
                }
                p {
                    font-size: 16px;
                    color: #555;
                }
                a {
                    text-decoration: none;
                    padding: 10px 20px;
                    font-size: 16px;
                    border-radius: 5px;
                    background-color: #007BFF;
                    color: white;
                    transition: background-color 0.3s;
                }
                a:hover {
                    background-color: #0056b3;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div style="position: fixed; top: 20px; right: 20px;">
                    <a href="{{ url_for('home') }}" 
                    style="text-decoration: none; 
                            background-color: #88d498; 
                            color: white; 
                            padding: 12px 24px; 
                            border-radius: 20px; 
                            font-size: 16px; 
                            font-weight: bold; 
                            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15); 
                            transition: background-color 0.3s, transform 0.2s;">
                        Home
                    </a>
                </div>
                <h1>Note Published in {{ branch }}</h1>
                <p>{{ note_content }}</p>
                <a href="{{ url_for('note_system') }}">Note System</a>
            </div>
        </body>
        </html>
    ''', branch=branch, note_content=note_content)

@app.route('/note_system')
def note_system():
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Note System</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f9f9f9;
                    margin: 0;
                    padding: 0;
                }
                .container {
                    background: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                    text-align: left;
                    max-width: 600px;
                    margin: 20px auto;
                    overflow-y: auto;
                    max-height: 90vh; /* Ensures the container is scrollable */
                }
                h1 {
                    color: #333;
                    text-align: center;
                    font-size: 24px;
                }
                ul {
                    list-style-type: none;
                    padding: 0;
                }
                li {
                    margin: 10px 0;
                }
                .subitem {
                    margin-left: 20px; /* Indents the subitems */
                    color: #555;
                }
                h2 a, h3 a {
                    text-decoration: none;
                    color: #007BFF;
                    transition: color 0.3s;
                }
                h2 a:hover, h3 a:hover {
                    color: #0056b3;
                }
                .home-link {
                    text-align: right;
                    margin-bottom: 20px;
                }
                .home-link a {
                    text-decoration: none;
                    color: #007BFF;
                }
                .home-link a:hover {
                    text-decoration: underline;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div style="position: fixed; top: 20px; right: 20px;">
                    <a href="{{ url_for('home') }}" 
                    style="text-decoration: none; 
                            background-color: #88d498; 
                            color: white; 
                            padding: 12px 24px; 
                            border-radius: 20px; 
                            font-size: 16px; 
                            font-weight: bold; 
                            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15); 
                            transition: background-color 0.3s, transform 0.2s;">
                        Home
                    </a>
                </div>
                <h1>Note System</h1>
                <ul>
                    {% for main_area, branches in knowledge_areas.items() %}
                        <li>
                            <h2><a href="{{ url_for('view_notes', area=main_area) }}">{{ main_area }}</a></h2>
                            <ul>
                                {% for branch in branches %}
                                    <li class="subitem"><h3><a href="{{ url_for('view_branch_notes', branch=branch) }}">{{ branch }}</a></h3></li>
                                {% endfor %}
                            </ul>
                        </li>
                    {% endfor %}
                </ul>
            </div>
        </body>
        </html>
    ''', knowledge_areas=knowledge_areas)

@app.route('/view_notes/<area>')
def view_notes(area):
    papers = notes.get(area, [])
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Notes in {{ area }}</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f9f9f9;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    flex-direction: column;
                }
                .container {
                    background: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                    text-align: center;
                    max-width: 600px;
                    width: 90%;
                }
                h1 {
                    color: #333;
                    font-size: 24px;
                }
                ul {
                    list-style-type: disc;
                    text-align: left;
                    padding: 0 20px;
                }
                li {
                    margin: 10px 0;
                    color: #555;
                }
                a {
                    text-decoration: none;
                    color: #007BFF;
                    margin-top: 10px;
                    display: inline-block;
                }
                a:hover {
                    text-decoration: underline;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Notes in {{ area }}</h1>
                <ul>
                    {% for paper in papers %}
                        <li>{{ paper }}</li>
                    {% endfor %}
                </ul>
                <a href="{{ url_for('note_system') }}">Back to Note System</a>
            </div>
        </body>
        </html>
    ''', area=area, papers=papers)

@app.route('/view_branch_notes/<branch>')
def view_branch_notes(branch):
    papers = notes.get(branch, [])
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Notes in {{ branch }}</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f9f9f9;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    flex-direction: column;
                }
                .container {
                    background: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                    text-align: center;
                    max-width: 600px;
                    width: 90%;
                }
                h1 {
                    color: #333;
                    font-size: 24px;
                }
                ul {
                    list-style-type: disc;
                    text-align: left;
                    padding: 0 20px;
                }
                li {
                    margin: 10px 0;
                    color: #555;
                }
                a {
                    text-decoration: none;
                    color: #007BFF;
                    margin-top: 10px;
                    display: inline-block;
                }
                a:hover {
                    text-decoration: underline;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Notes in {{ branch }}</h1>
                <ul>
                    {% for paper in papers %}
                        <li>{{ paper }}</li>
                    {% endfor %}
                </ul>
                <a href="{{ url_for('note_system') }}">Back to Note System</a>
            </div>
        </body>
        </html>
    ''', branch=branch, papers=papers)

@app.route('/study_system', methods=['GET', 'POST'])
def study_system():
    if request.method == 'POST':
        chosen_topic = request.form['topic']
        if chosen_topic in rules:
            rule = random.choice(rules[chosen_topic])
            return render_template_string('''
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Study System</title>
                    <style>
                        body {
                            font-family: Arial, sans-serif;
                            background-color: #f0f8ff;
                            margin: 0;
                            padding: 0;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            height: 100vh;
                            flex-direction: column;
                        }
                        .container {
                            background: white;
                            padding: 20px;
                            border-radius: 10px;
                            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                            text-align: center;
                            max-width: 400px;
                            width: 90%;
                        }
                        h1 {
                            color: #333;
                            font-size: 24px;
                        }
                        p {
                            color: #555;
                            font-size: 18px;
                        }
                        button {
                            margin: 5px;
                            padding: 10px 20px;
                            font-size: 16px;
                            border: none;
                            border-radius: 5px;
                            background-color: #007BFF;
                            color: white;
                            cursor: pointer;
                            transition: background-color 0.3s;
                        }
                        button:hover {
                            background-color: #0056b3;
                        }
                        .home-link {
                            text-decoration: none;
                            color: #007BFF;
                            margin-top: 10px;
                            display: inline-block;
                        }
                        .home-link:hover {
                            text-decoration: underline;
                        }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>Study System</h1>
                        <p><strong>Topic:</strong> {{ chosen_topic }}</p>
                        <p><strong>Rule:</strong> {{ rule }}</p>
                        <form method="post" action="/study_system">
                            <input type="hidden" name="topic" value="{{ chosen_topic }}">
                            <button type="submit" name="action" value="master">Master</button>
                            <button type="submit" name="action" value="forget">Forget</button>
                        </form>
                        <div style="position: fixed; top: 20px; right: 20px;">
                            <a href="{{ url_for('home') }}" 
                            style="text-decoration: none; 
                                    background-color: #88d498; 
                                    color: white; 
                                    padding: 12px 24px; 
                                    border-radius: 20px; 
                                    font-size: 16px; 
                                    font-weight: bold; 
                                    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15); 
                                    transition: background-color 0.3s, transform 0.2s;">
                                Home
                            </a>
                        </div>
                    </div>
                </body>
                </html>
            ''', chosen_topic=chosen_topic, rule=rule)

    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Study System</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f0f8ff;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    flex-direction: column;
                }
                .container {
                    background: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                    text-align: center;
                    max-width: 400px;
                    width: 90%;
                }
                h1 {
                    color: #333;
                    font-size: 24px;
                }
                form {
                    margin-top: 20px;
                }
                select {
                    padding: 10px;
                    font-size: 16px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    width: 100%;
                    margin-bottom: 20px;
                }
                button {
                    padding: 10px 20px;
                    font-size: 16px;
                    border: none;
                    border-radius: 5px;
                    background-color: #007BFF;
                    color: white;
                    cursor: pointer;
                    transition: background-color 0.3s;
                }
                button:hover {
                    background-color: #0056b3;
                }
                .home-link {
                    text-decoration: none;
                    color: #007BFF;
                    margin-top: 10px;
                    display: inline-block;
                }
                .home-link:hover {
                    text-decoration: underline;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Study System</h1>
                <form method="post" action="/study_system">
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
                <div style="position: fixed; top: 20px; right: 20px;">
                    <a href="{{ url_for('home') }}" 
                    style="text-decoration: none; 
                            background-color: #88d498; 
                            color: white; 
                            padding: 12px 24px; 
                            border-radius: 20px; 
                            font-size: 16px; 
                            font-weight: bold; 
                            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15); 
                            transition: background-color 0.3s, transform 0.2s;">
                        Home
                    </a>
                </div>
            </div>
        </body>
        </html>
    ''', knowledge_areas=knowledge_areas)

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
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Exam System</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f0f8ff; margin: 0; padding: 0; }
            .container { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); text-align: center; max-width: 400px; width: 90%; margin: 50px auto; }
            h1 { color: #333; font-size: 24px; }
            select, button { padding: 10px; font-size: 16px; margin-top: 20px; width: 100%; }
            a { text-decoration: none; color: #88d498; font-weight: bold; }
        </style>
    </head>
    <body>
        <div style="position: fixed; top: 20px; right: 20px;">
            <a href="{{ url_for('home') }}" 
               style="text-decoration: none; 
                      background-color: #88d498; 
                      color: white; 
                      padding: 12px 24px; 
                      border-radius: 20px; 
                      font-size: 16px; 
                      font-weight: bold; 
                      box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15); 
                      transition: background-color 0.3s, transform 0.2s;">
                Home
            </a>
        </div>
        <div class="container">
            <h1>Exam System</h1>
            <form method="post" action="/exam_system">
                <select name="topic">
                    {% for function, branches in knowledge_areas.items() %}
                        <option value="{{ function }}">{{ function }}</option>
                        {% for branch in branches %}
                            <option value="{{ branch }}">-- {{ branch }}</option>
                        {% endfor %}
                    {% endfor %}
                </select>
                <button type="submit">Start Exam</button>
            </form>
        </div>
    </body>
    </html>
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
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Take Exam</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f0f8ff; margin: 0; padding: 0; }
            .container { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); text-align: center; max-width: 400px; width: 90%; margin: 50px auto; }
            h1 { color: #333; font-size: 24px; }
            p { font-size: 18px; color: #555; }
            button { padding: 10px; font-size: 16px; margin: 10px; width: 45%; }
            a { text-decoration: none; color: #88d498; font-weight: bold; }
        </style>
    </head>
    <body>
        <div style="position: fixed; top: 20px; right: 20px;">
            <a href="{{ url_for('home') }}" 
               style="text-decoration: none; 
                      background-color: #88d498; 
                      color: white; 
                      padding: 12px 24px; 
                      border-radius: 20px; 
                      font-size: 16px; 
                      font-weight: bold; 
                      box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15); 
                      transition: background-color 0.3s, transform 0.2s;">
                Home
            </a>
        </div>
        <div class="container">
            <h1>Take Exam</h1>
            <p><strong>Question:</strong> {{ current_question }}</p>
            <form method="post" action="/take_exam">
                <button type="submit" name="action" value="correct">Correct</button>
                <button type="submit" name="action" value="incorrect">Incorrect</button>
            </form>
        </div>
    </body>
    </html>
    ''', current_question=current_question)

@app.route('/exam_result')
def exam_result():
    score = session.get('score', 0)
    result = "Pass" if score >= 80 else "Fail"
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Exam Result</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f0f8ff; margin: 0; padding: 0; }
            .container { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); text-align: center; max-width: 400px; width: 90%; margin: 50px auto; }
            h1 { color: #333; font-size: 24px; }
            p { font-size: 18px; color: #555; }
            a { text-decoration: none; padding: 10px 20px; font-size: 16px; border-radius: 5px; background-color: #88d498; color: white; text-align: center; margin-top: 20px; display: inline-block; transition: background-color 0.3s; }
            a:hover { background-color: #66c282; }
        </style>
    </head>
    <body>
        <div style="position: fixed; top: 20px; right: 20px;">
            <a href="{{ url_for('home') }}" 
               style="text-decoration: none; 
                      background-color: #88d498; 
                      color: white; 
                      padding: 12px 24px; 
                      border-radius: 20px; 
                      font-size: 16px; 
                      font-weight: bold; 
                      box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15); 
                      transition: background-color 0.3s, transform 0.2s;">
                Home
            </a>
        </div>
        <div class="container">
            <h1>Exam Result</h1>
            <p>Your score: <strong>{{ score }}</strong></p>
            <p>Result: <strong>{{ result }}</strong></p>
            <a href="{{ url_for('exam_system') }}">Back to Exam System</a>
        </div>
    </body>
    </html>
    ''', score=score, result=result)


@app.route('/Social_Chat', methods=['GET', 'POST'])
def social_chat():
    def validate_uid(uid):
        """Validate UID format"""
        return uid.isalnum()
    
    if request.method == 'POST' and 'uid' in request.form:
        uid = request.form['uid']
        
        # Validate UID
        if not validate_uid(uid):
            return "Invalid UID! UID must be alphanumeric.", 400

        return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Social Chat</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body { background-color: #f9f9f9; }
                .chat-container { margin: 20px auto; max-width: 600px; background: #fff; border-radius: 8px; padding: 20px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); }
                .chat-header { text-align: center; padding: 10px 0; }
                .chat-messages { max-height: 300px; overflow-y: auto; margin-bottom: 20px; }
                .chat-messages ul { list-style: none; padding: 0; }
                .chat-messages li { background: #e9f5ff; margin-bottom: 10px; padding: 10px; border-radius: 5px; }
                .chat-input { display: flex; gap: 10px; }
                .chat-input input { flex: 1; }
            </style>
        </head>
        <body>
            <div style="position: fixed; top: 20px; right: 20px;">
                <a href="{{ url_for('home') }}" 
                   style="text-decoration: none; 
                          background-color: #88d498; 
                          color: white; 
                          padding: 12px 24px; 
                          border-radius: 20px; 
                          font-size: 16px; 
                          font-weight: bold; 
                          box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15); 
                          transition: background-color 0.3s, transform 0.2s;">
                    Home
                </a>
            </div>
            <div class="container chat-container">
                <div class="chat-header">
                    <h1>Chat with {{ uid }}</h1>
                </div>
                <div class="chat-messages">
                    <ul id="messages">
                        {% for message in chat_history.get(uid, []) %}
                            <li>{{ message }}</li>
                        {% endfor %}
                    </ul>
                </div>
                <div class="chat-input">
                    <input id="message" type="text" class="form-control" placeholder="Type your message here...">
                    <button class="btn btn-primary" onclick="sendMessage()">Send</button>
                </div>
            </div>
            <script src="https://cdn.jsdelivr.net/npm/socket.io-client/dist/socket.io.min.js"></script>
            <script>
                var socket = io();
                var uid = "{{ uid }}";
                socket.emit('join', uid);
                socket.on('message', function(msg){
                    var li = document.createElement("li");
                    li.textContent = msg;
                    document.getElementById("messages").appendChild(li);
                });
                function sendMessage() {
                    var msg = document.getElementById("message").value;
                    socket.emit('message', {uid: uid, msg: msg});
                    document.getElementById("message").value = '';  // Clear input after sending
                }
            </script>
        </body>
        </html>
        ''', uid=uid, chat_history=chat_history)

    # Default chat form
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Social Chat</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background-color: #f9f9f9; }
            .form-container { margin: 100px auto; max-width: 400px; background: #fff; border-radius: 8px; padding: 20px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); }
            .form-header { text-align: center; margin-bottom: 20px; }
        </style>
    </head>
    <body>
        <div style="position: fixed; top: 20px; right: 20px;">
            <a href="{{ url_for('home') }}" 
               style="text-decoration: none; 
                      background-color: #88d498; 
                      color: white; 
                      padding: 12px 24px; 
                      border-radius: 20px; 
                      font-size: 16px; 
                      font-weight: bold; 
                      box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15); 
                      transition: background-color 0.3s, transform 0.2s;">
                Home
            </a>
        </div>
        <div class="container form-container">
            <div class="form-header">
                <h1>Social Chat</h1>
            </div>
            <form method="post" action="/Social_Chat">
                <div class="mb-3">
                    <label for="uid" class="form-label">Enter UID</label>
                    <input type="text" id="uid" name="uid" class="form-control" required>
                </div>
                <button type="submit" class="btn btn-primary w-100">Start Chat</button>
            </form>
        </div>
    </body>
    </html>
    ''')

@app.route('/Social_Pay', methods=['GET', 'POST'])
def social_pay():
    if request.method == 'POST' and 'uid' in request.form:
        uid = request.form['uid']

        # Initialize user balance and payment history if the user is new
        if uid not in user_balances:
            user_balances[uid] = random.randint(0, 100_000)
            payment_history[uid] = []

        user_balance = user_balances[uid]
        user_history = payment_history[uid]

        return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Social Pay</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body { background-color: #f8f9fa; }
                .container { max-width: 600px; margin: 40px auto; padding: 20px; background: #fff; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); }
                h1, h2, h3 { color: #333; }
                ul { list-style-type: none; padding: 0; }
                li { background-color: #e9f5ff; padding: 10px; margin-bottom: 5px; border-radius: 5px; }
                .alert { margin-top: 20px; }
            </style>
        </head>
        <body>
            <div style="position: fixed; top: 20px; right: 20px;">
                <a href="{{ url_for('home') }}" 
                   style="text-decoration: none; 
                          background-color: #88d498; 
                          color: white; 
                          padding: 12px 24px; 
                          border-radius: 20px; 
                          font-size: 16px; 
                          font-weight: bold; 
                          box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15); 
                          transition: background-color 0.3s, transform 0.2s;">
                    Home
                </a>
            </div>
            <div class="container text-center">
                <h1>Payment to <span class="text-primary">{{ uid }}</span></h1>
                <h2>Balance: $<span id="balance" class="text-success">{{ "{:,}".format(user_balance) }}</span></h2>
                <h3>Payment History</h3>
                <ul id="history" class="list-group">
                    {% for record in user_history %}
                        <li class="list-group-item">{{ record }}</li>
                    {% endfor %}
                </ul>
                <div class="mt-4">
                    <label for="amount" class="form-label">Amount:</label>
                    <input id="amount" type="number" step="1" class="form-control" placeholder="Enter amount">
                    <button class="btn btn-primary mt-3" onclick="sendPayment()">Pay</button>
                </div>
                <div id="alert-container" class="mt-3"></div>
            </div>
            <script src="https://cdn.jsdelivr.net/npm/socket.io-client/dist/socket.io.min.js"></script>
            <script>
                var socket = io();
                var uid = "{{ uid }}";

                // Join the room for this user
                socket.emit('join', uid);

                // Listen for balance updates
                socket.on('update_balance', function(data) {
                    if (data.uid === uid) {
                        // Update balance
                        document.getElementById("balance").textContent = data.balance.toLocaleString();

                        // Update payment history
                        const historyList = document.getElementById("history");
                        historyList.innerHTML = ""; // Clear existing history
                        data.history.forEach(record => {
                            const li = document.createElement("li");
                            li.textContent = record;
                            li.classList.add('list-group-item');
                            historyList.appendChild(li);
                        });

                        showAlert("Payment successful!", "success");
                    }
                });

                // Send payment request
                function sendPayment() {
                    var amount = document.getElementById("amount").value;
                    if (amount && parseInt(amount) > 0) {
                        socket.emit('payment', {uid: uid, amount: parseInt(amount)});
                        document.getElementById("amount").value = ''; // Clear input
                    } else {
                        showAlert("Please enter a valid amount!", "danger");
                    }
                }

                // Show alert messages
                function showAlert(message, type) {
                    const alertContainer = document.getElementById("alert-container");
                    alertContainer.innerHTML = `
                        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                            ${message}
                            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                        </div>
                    `;
                }
            </script>
        </body>
        </html>
        ''', uid=uid, user_balance=user_balance, user_history=user_history)

    # Default payment form
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Social Pay</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background-color: #f8f9fa; }
            .container { max-width: 400px; margin: 100px auto; padding: 20px; background: #fff; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); }
        </style>
    </head>
    <body>
        <div style="position: fixed; top: 20px; right: 20px;">
            <a href="{{ url_for('home') }}" 
               style="text-decoration: none; 
                      background-color: #88d498; 
                      color: white; 
                      padding: 12px 24px; 
                      border-radius: 20px; 
                      font-size: 16px; 
                      font-weight: bold; 
                      box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15); 
                      transition: background-color 0.3s, transform 0.2s;">
                Home
            </a>
        </div>
        <div class="container text-center">
            <h1>Social Pay</h1>
            <form method="post" action="/Social_Pay">
                <div class="mb-3">
                    <label for="uid" class="form-label">Enter UID:</label>
                    <input type="text" id="uid" name="uid" class="form-control" required>
                </div>
                <button type="submit" class="btn btn-primary w-100">Start Payment</button>
            </form>
        </div>
    </body>
    </html>
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


@socketio.on('payment')
def handle_payment(data):
    uid = data['uid']
    amount = data.get('amount', 0.0)

    if not amount or amount <= 0:
        send({"message": "Invalid payment amount!"}, to=uid)
        return

    # Initialize balance and history if user is new
    if uid not in user_balances:
        user_balances[uid] = random.randint(0, 100_000)  # Random balance
        payment_history[uid] = []

    # Update balance and payment history
    user_balances[uid] += amount
    payment_record = f"Received ${int(amount):,}"
    payment_history[uid].append(payment_record)

    # Emit the updated balance and history to the client
    socketio.emit('update_balance', {
        'uid': uid,
        'balance': user_balances[uid],
        'history': payment_history[uid]
    }, to=uid)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5010, debug=True)

