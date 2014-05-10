from __future__ import print_function
from jinja2 import Environment, FileSystemLoader
from pprint import pprint
import argparse
import json
import requests
import os

def read_config(cfg_filename):
    with open(cfg_filename) as cfg_f:
        cfg = json.loads(cfg_f.read())

    return cfg['pi-web-agent']['system']['actions']

def time_actions(actions, root_url):
    action_times = {}
    password = raw_input("Please provide the password: ")
    for action, attrs in actions.iteritems():
        action_url = "".join([root_url, attrs['url']])
        dt = requests.get(action_url, verify=False,
                          auth=('admin', password)).elapsed.total_seconds()
        action_times[attrs['title']] = dt
        print("finished ", action_url, " in ", dt, " seconds!")

    return action_times

def run_tests(config_filename, root_url):
    actions = read_config(config_filename)
    action_times = time_actions(actions, root_url)
    
    return action_times

def write_results(action_times, fout_name):
    env = Environment(loader=FileSystemLoader(searchpath='templates'))
    template = env.get_template('results.html')

    try:
        os.remove(fout_name)
    except OSError:
        pass
        
    with open(fout_name, "w") as fout:
        fout.write(template.render(action_times=json.dumps(action_times)))

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--root",
                        help="URL for pi-web-agent",
                        required=True)
    parser.add_argument("-o", "--fout",
                        help="Name for html file output",
                        required=False, default="results_rend.html")

    parser.add_argument("-c", "--cfg",
                        help="Location of configuration file containing actions to test",
                        required=False, default="config.cfg")
    return parser
    
def command_line_runner():
    parser = get_parser()
    args = parser.parse_args()
    
    action_times = run_tests(config_filename=args.cfg, root_url=args.root)
    write_results(action_times, args.fout)
    
if __name__ == "__main__":
    command_line_runner()
