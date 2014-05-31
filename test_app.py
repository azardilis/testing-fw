import os
from flask import Flask, render_template
from test_framework import run_tests
import json
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

@app.route("/")
def run_test():
    action_times = run_tests("config.cfg", "https://192.168.2.10:8003")
    return render_template('results.html', action_times=json.dumps(action_times))
    

if __name__ == "__main__":
    app.run()
