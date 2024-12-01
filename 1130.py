from flask import Flask, render_template_string, request

app = Flask(__name__)

functions = [
    "Function 1",
    "Function 2",
    "Function 3",
    "Function 4",
    "Function 5",
    "Function 6",
    "Function 7",
    "Function 8",
    "Function 9",
    "Function 10"
]

@app.route('/')
def home():
    return render_template_string('''
        <h1>Choose a Function</h1>
        <form method="post" action="/choose">
            {% for function in functions %}
                <button type="submit" name="function" value="{{ function }}">{{ function }}</button>
            {% endfor %}
        </form>
    ''', functions=functions)

@app.route('/choose', methods=['POST'])
def choose():
    chosen_function = request.form['function']
    return render_template_string('''
        <h1>{{ chosen_function }}</h1>
        <p>You have chosen: {{ chosen_function }}</p>
        <a href="/">Go back</a>
    ''', chosen_function=chosen_function)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)