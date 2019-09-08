from flask import Flask, render_template, request
import subprocess, serial.tools.list_ports, json, os, re, shutil
import configparser
import webrepl_cli
import requests
import websocket

import devices

app = Flask(__name__)

global_config = configparser.ConfigParser()
global_config.read('../config.ini')

device_dict = devices.get_devices()

@app.route('/')
def index():
    return render_template('index.html', remote_processors=get_remote_processors())

def get_remote_processors():
    result = {}
    config = configparser.ConfigParser()
    for directory in [f.path for f in os.scandir('./devices') if f.is_dir()]:
        config.read(directory + '/config.ini')
        result[int(config["INFO"]["id"])] = {x:dict(config._sections[x]) for x in config._sections}
        result[int(config["INFO"]["id"])]["callables"] = json.loads(open(directory + '/device.json').read())

    return result

# ESP32
from blueprints.remote_processor.remote_processor import remote_processor
app.register_blueprint(remote_processor)

# Google Assistant
@app.route('/action_package/add')
def add_action_package():
    triggerHTML = open("templates/snippets/add_action_package/action/trigger/pattern.html", "r").read().replace('\n', '').replace('\r', '').replace('"', '\\"')
    parameterHTML = open("templates/snippets/add_action_package/action/parameters/parameter.html", "r").read().replace('\n', '').replace('\r', '').replace('"', '\\"')
    keyHTML = open("templates/snippets/add_action_package/action/parameters/key.html", "r").read().replace('\n', '').replace('\r', '').replace('"', '\\"')

    supportedTypes = ['Number', 'Text', 'Yes/No', 'URL', 'Email', 'Phone Number', 'Date', 'Time', 'DateTime', 'Day of the Week', 'Colour', 'Currency', 'Distance', 'Temperature', 'Organisation', 'Person', 'Place', 'Product', 'Book', 'Movie', 'TV Series', 'Cuisine', 'Music Album', 'Music Recording']

    device_manifest = get_remote_processors()
    print(device_manifest)

    return render_template('add_action_package.html', triggerHTML=triggerHTML, parameterHTML=parameterHTML, keyHTML=keyHTML, supportedTypes=supportedTypes, device_manifest=device_manifest)

@app.route('/action_package/add/create', methods=['POST'])
def create_Action_package():
    print(request.values)

@app.route('/is-assistant-running')
def is_assistant_running():
    try:
        return "Running" if 'active (running)' in str(subprocess.check_output("systemctl status assistant.service", shell=True)) else "Halted"
    except:
        return "Halted"

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
