from flask import Flask, render_template
from test_framework import run_tests
import json

app = Flask(__name__)

@app.route("/")
def run_test():
    action_times = run_tests("config.cfg", "https://192.168.56.101:8003")
    
    return render_template('results.html', action_times=json.dumps(action_times))
    

if __name__ == "__main__":
    app.run()
