from flask import Blueprint, render_template, request
import serial.tools.list_ports, json
import esptool

remote_processor = Blueprint('remote_processor', __name__,
                            template_folder='templates',
                            static_folder='static')

@remote_processor.route('/remote-processor/setup')
def setup_remote_processor():
    return render_template('setup.html')

@remote_processor.route('/remote-processor/program/<id>')
def program_remote_processor(id):
    return render_template('program.html', id=id)

@remote_processor.route('/remote-processor/upload/<id>', methods=['POST'])
def upload_to_remote_processor(id):
    remote_device = get_remote_processors()[int(id)]
    code = request.values["code"]

    # Store the user's code in a file
    file = open('devices/' + str(id) + '/user.py', 'w')
    file.write(code)
    file.close()
    shutil.copyfile('devices/' + str(id) + '/user.py', 'static/devices/' + str(id) + '/user.py')

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

    # Update the device's json file
    open('devices/' + str(id) + '/device.json', 'w').write(json.dumps(callables))

    device_dict[int(id)].upload('devices/' + str(id) + '/user.py', 'user.py')
    device_dict[int(id)].reset()

    return json.dumps(callables)

@remote_processor.route('/remote-processor/get_callables/<id>')
def remote_processor_get_callables(id):
    code = open('devices/' + str(id) + '/user.py').read()
    all_routines = re.findall("def .*", code)
    callables = {}
    for routine in all_routines:
        routine_name = routine[routine.index("def ")+4:routine.index("(")].strip()
        args = routine[routine.find("(") + 1:routine.find(")")]
        callables[routine_name] = args.split(",")
        callables[routine_name] = [x.strip() for x in callables[routine_name]]
        if callables[routine_name] == ['']:
            callables[routine_name] = []

    return json.dumps(callables)

@remote_processor.route('/remote-processor/test/<id>/<function>', methods=['POST'])
def test_remote_processor(id, function):
    command = "result = device_dict[int(id)]." + function + "("
    print(request.json)
    for arg in request.json:
        command += request.json[arg] + ","
    command += ")"
    exec(command)
    return result

all_ports = None
@remote_processor.route('/remote-processor/setup/1-1')
def setup_remote_processor_1_1():
    global all_ports
    all_ports = [port.name for port in serial.tools.list_ports.comports()]
    return json.dumps(True)

@remote_processor.route('/remote-processor/setup/1-2')
def setup_remote_processor_1_2():
    not_in_both = []
    for port in [port.name for port in serial.tools.list_ports.comports()]:
        if not port in all_ports:
            not_in_both.append(port)
    if len(not_in_both) != 1:
        return json.dumps(False)
    else:
        return json.dumps(not_in_both[0])

@remote_processor.route('/remote-processor/setup/1-3', methods=['POST'])
def setup_remote_processor_1_3():
    try:
        esptool.main(custom_commandline=['--port', '/dev/' + request.values["port"], 'erase_flash'])
        esptool.main(custom_commandline=['--port', '/dev/' + request.values["port"], 'write_flash', '-z', '0x1000', 'esp-32-img.bin'])
    except BaseException as ex:
        print(ex)
        return json.dumps(ex)
    return json.dumps(True)

@remote_processor.route('/remote-processor/setup/2-1/<name>')
def setup_remote_processor_2_1(name):
    os.mkdir("devices/" + name)
    config = configparser.ConfigParser()
    config['INFO'] = {'name': name}
    with open('devices/' + name + '/config.ini', 'w') as configfile:
        config.write(configfile)
