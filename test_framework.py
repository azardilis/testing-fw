from __future__ import print_function
from pprint import pprint
from jinja2 import Environment, FileSystemLoader
import json
import requests

def read_config(cfg_filename):
    with open(cfg_filename) as cfg_f:
        cfg = json.loads(cfg_f.read())

    return cfg['pi-web-agent']['system']['actions']

def time_actions(actions):
    action_times = {}
    ROOT = raw_input("Please provide the ip address: ")
    password = raw_input("Please provide the password: ")
    for action, attrs in actions.iteritems():
        action_url = "".join([ROOT, attrs['url']])
        dt = requests.get(action_url, verify=False, auth=('admin', password)).elapsed.total_seconds()
        action_times[attrs['title']] = dt
        print("finished ", action_url, " in ", dt, " seconds!")
    return action_times

def main():
    actions = read_config("config.cfg")
    action_times = time_actions(actions)
    #pprint(json.dumps(action_times))

    env = Environment(loader=FileSystemLoader(searchpath='templates'))
    template = env.get_template('results.html')

    with open("rendered.html", "w") as fout:
        fout.write(template.render(action_times=action_times))

if __name__ == "__main__":
    main()
