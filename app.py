from flask import Flask, render_template, request
from model import TaskManager

app = Flask(__name__)
manager = TaskManager()  # Initialize the TaskManager once

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    task_input = ""
    
    if request.method == "POST":
        task_input = request.form.get("task")
        if task_input:
            input_data = {"tasks": [task_input]}
            result = manager.run(input_data)

    return render_template("index.html", task=task_input, result=result)

if __name__ == "__main__":
    app.run(debug=True)
