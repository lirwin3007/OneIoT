from flask import Flask, render_template, request
import subprocess, serial.tools.list_ports, json, os
import esptool
import configparser

#from PyAccessPoint import pyaccesspoint
#access_point = pyaccesspoint.AccessPoint(ssid='OneIoT', password='oneiot')
#access_point.start()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# ESP32
@app.route('/remote-processor/setup')
def setup_remote_processor():
    return render_template('setup_remote_processor.html')

all_ports = None

@app.route('/remote-processor/setup/1-1')
def setup_remote_processor_1_1():
    global all_ports
    all_ports = [port.name for port in serial.tools.list_ports.comports()]
    return json.dumps(True)

@app.route('/remote-processor/setup/1-2')
def setup_remote_processor_1_2():
    not_in_both = []
    for port in [port.name for port in serial.tools.list_ports.comports()]:
        if not port in all_ports:
            not_in_both.append(port)
    if len(not_in_both) != 1:
        return json.dumps(False)
    else:
        return json.dumps(not_in_both[0])

@app.route('/remote-processor/setup/1-3', methods=['POST'])
def setup_remote_processor_1_3():
    try:
        esptool.main(custom_commandline=['--port', '/dev/' + request.values["port"], 'erase_flash'])
        esptool.main(custom_commandline=['--port', '/dev/' + request.values["port"], 'write_flash', '-z', '0x1000', 'esp-32-img.bin'])
    except BaseException as ex:
        print(ex)
        return json.dumps(ex)
    return json.dumps(True)

@app.route('/remote-processor/setup/2-1/<name>')
def setup_remote_processor_2_1(name):
    os.mkdir("devices/" + name)
    config = configparser.ConfigParser()
    config['INFO'] = {'name': name}
    with open('devices/' + name + '/config.ini', 'w') as configfile:
        config.write(configfile)

# Google Assistant
@app.route('/action_package/add')
def add_action_package():
    triggerHTML = open("templates/snippets/add_action_package/action/trigger/pattern.html", "r").read().replace('\n', '').replace('\r', '').replace('"', '\\"')
    parameterHTML = open("templates/snippets/add_action_package/action/parameters/parameter.html", "r").read().replace('\n', '').replace('\r', '').replace('"', '\\"')
    keyHTML = open("templates/snippets/add_action_package/action/parameters/key.html", "r").read().replace('\n', '').replace('\r', '').replace('"', '\\"')

    supportedTypes = ['Number', 'Text', 'Yes/No', 'URL', 'Email', 'Phone Number', 'Date', 'Time', 'DateTime', 'Day of the Week', 'Colour', 'Currency', 'Distance', 'Temperature', 'Organisation', 'Person', 'Place', 'Product', 'Book', 'Movie', 'TV Series', 'Cuisine', 'Music Album', 'Music Recording']

    return render_template('add_action_package.html', triggerHTML=triggerHTML, parameterHTML=parameterHTML, keyHTML=keyHTML, supportedTypes=supportedTypes)

@app.route('/is-assistant-running')
def is_assistant_running():
    try:
        return "Running" if 'active (running)' in str(subprocess.check_output("systemctl status assistant.service", shell=True)) else "Halted"
    except:
        return "Halted"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
