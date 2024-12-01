from flask import Flask, render_template_string, request

app = Flask(__name__)

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
    "English": [
        "Grammar",
        "Literature",
        "Writing",
        "Poetry",
        "Linguistics",
        "Phonetics",
        "Syntax",
        "Semantics",
        "Rhetoric",
        "Composition"
    ],
    "Science": [
        "Physics",
        "Chemistry",
        "Biology",
        "Astronomy",
        "Geology",
        "Meteorology",
        "Ecology",
        "Botany",
        "Zoology",
        "Genetics"
    ],
    "History": [
        "Ancient History",
        "Medieval History",
        "Modern History",
        "World History",
        "American History",
        "European History",
        "Asian History",
        "African History",
        "Middle Eastern History",
        "Latin American History"
    ],
    "Geography": [
        "Physical Geography",
        "Human Geography",
        "Cartography",
        "Geology",
        "Climatology",
        "Biogeography",
        "Urban Geography",
        "Economic Geography",
        "Political Geography",
        "Cultural Geography"
    ],
    "Art": [
        "Painting",
        "Sculpture",
        "Drawing",
        "Photography",
        "Printmaking",
        "Ceramics",
        "Textile Arts",
        "Digital Art",
        "Performance Art",
        "Installation Art"
    ],
    "Music": [
        "Classical Music",
        "Jazz",
        "Rock",
        "Pop",
        "Hip Hop",
        "Electronic Music",
        "Folk Music",
        "Blues",
        "Country Music",
        "Reggae"
    ],
    "Physical Education": [
        "Exercise Physiology",
        "Kinesiology",
        "Sports Psychology",
        "Motor Learning",
        "Biomechanics",
        "Sports Nutrition",
        "Athletic Training",
        "Health Education",
        "Recreation",
        "Outdoor Education"
    ],
    "Computer Science": [
        "Algorithms",
        "Data Structures",
        "Operating Systems",
        "Computer Networks",
        "Databases",
        "Artificial Intelligence",
        "Machine Learning",
        "Software Engineering",
        "Cybersecurity",
        "Human-Computer Interaction"
    ],
    "Economics": [
        "Microeconomics",
        "Macroeconomics",
        "International Economics",
        "Development Economics",
        "Behavioral Economics",
        "Labor Economics",
        "Public Economics",
        "Health Economics",
        "Environmental Economics",
        "Econometrics"
    ]
}

@app.route('/')
def home():
    sorted_functions = sorted(functions)
    return render_template_string('''
        <h1>Choose a Knowledge Area</h1>
        <form method="post" action="/choose">
            {% for function in sorted_functions %}
                <button type="submit" name="function" value="{{ function }}">{{ function }}</button>
            {% endfor %}
        </form>
    ''', sorted_functions=sorted_functions)

@app.route('/choose', methods=['POST'])
def choose():
    chosen_function = request.form['function']
    branches = knowledge_areas.get(chosen_function, ["No branches available."])
    return render_template_string('''
        <h1>{{ chosen_function }}</h1>
        <form method="post" action="/branch">
            {% for branch in branches %}
                <button type="submit" name="branch" value="{{ branch }}">{{ branch }}</button>
            {% endfor %}
        </form>
        <a href="/">Go back</a>
    ''', chosen_function=chosen_function, branches=branches)

@app.route('/branch', methods=['POST'])
def branch():
    chosen_branch = request.form['branch']
    return render_template_string('''
        <h1>{{ chosen_branch }}</h1>
        <p>Content for {{ chosen_branch }}</p>
        <a href="/">Go back</a>
    ''', chosen_branch=chosen_branch)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)