from flask import Flask, render_template, request
import subprocess, serial.tools.list_ports, json, os, re, shutil
import esptool
import configparser
import webrepl_cli
import requests

#from PyAccessPoint import pyaccesspoint
#access_point = pyaccesspoint.AccessPoint(ssid='OneIoT', password='oneiot')
#access_point.start()

app = Flask(__name__)

global_config = configparser.ConfigParser()
global_config.read('../config.ini')

@app.route('/')
def index():
    return render_template('index.html', remote_processors=get_remote_processors())

def get_remote_processors():
    result = {}
    config = configparser.ConfigParser()
    for directory in [f.path for f in os.scandir('./devices') if f.is_dir()]:
        config.read(directory + '/config.ini')
        result[config["INFO"]["id"]] = config._sections
    return result

# ESP32
@app.route('/remote-processor/setup')
def setup_remote_processor():
    return render_template('setup_remote_processor.html')

@app.route('/remote-processor/program/<id>')
def program_remote_processor(id):
    return render_template('program_remote_processor.html', id=id)

@app.route('/remote-processor/upload/<id>', methods=['POST'])
def upload_to_remote_processor(id):
    remote_device = get_remote_processors()[id]
    code = request.values["code"]
    print(code)

    # Store the user's code in a file
    file = open('devices/' + str(id) + '/user.py', 'w')
    file.write(code)
    file.close()

    # Parse the user's code for routines
    all_routines = re.findall("def .*", code)
    callables = {}
    for routine in all_routines:
        routine_name = routine[routine.index("def ")+4:routine.index("(")].strip()
        args = routine[routine.find("(") + 1:routine.find(")")]
        callables[routine_name] = args.split(",")
        callables[routine_name] = [x.strip() for x in callables[routine_name]]
        if callables[routine_name] == ['']:
            callables[routine_name] = []
    print(callables)

    # Fill out templated details on source files
    shutil.copyfile('devices/boot_template.py', 'devices/' + str(id) + '/boot.py')
    boot_file = open('devices/' + str(id) + '/boot.py').read()
    boot_file = boot_file.replace('{{SSID}}', global_config['wireless-info']['ssid'])
    boot_file = boot_file.replace('{{PSK}}', global_config['wireless-info']['psk'])
    boot_file = boot_file.replace('{{IP_ADDRESS}}', remote_device['INFO']['ip'])
    open('devices/' + str(id) + '/boot.py', 'w').write(boot_file)

    shutil.copyfile('devices/main_template.py', 'devices/' + str(id) + '/main.py')
    main_file = open('devices/' + str(id) + '/main.py').read()
    main_file = main_file.replace('{{CALLABLES}}', str(callables))
    open('devices/' + str(id) + '/main.py', 'w').write(main_file)

    # Kill the currently running program
    requests.get(url="http://" + remote_device['INFO']['ip'] + "/kill_for_program_flash")

    # Upload the user's files
    webrepl_cli.main('OneIoT', '192.168.4.7:boot.py', 'put', src_file = 'devices/' + str(id) + '/boot.py')
    webrepl_cli.main('OneIoT', '192.168.4.7:main.py', 'put', src_file = 'devices/' + str(id) + '/main.py')
    webrepl_cli.main('OneIoT', '192.168.4.7:user.py', 'put', src_file = 'devices/' + str(id) + '/user.py')

    return "true"

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
