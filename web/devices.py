import os, configparser, json
import requests
import websocket
import webrepl_cli

def get_devices():
    result = {}
    config = configparser.ConfigParser()
    for directory in [f.path for f in os.scandir('./devices') if f.is_dir()]:
        config.read(directory + '/config.ini')
        result[int(config["INFO"]["id"])] = device(dict(config.items("INFO")), json.loads(open(directory + '/device.json').read()))
    return result

class callableFunction:
    def __init__(self, name, args, device):
        self.name = name
        self.args = args
        self.device = device

    def __call__(self, *argv):
        if len(argv) != len(self.args):
            raise ValueError("Incorrect number of arguments. " + str(len(self.args)) + " requrired, " + str(len(argv)) + " supplied")
        arg_dict = {self.args[i]:argv[i] for i in range(0, len(argv))}
        arg_string = ""
        for arg in argv:
            arg_string += str(arg) + ","
        command = "json.dumps(user." + self.name + "(" + arg_string + "))"
        self.device.ws.send(command + "\r\n")
        for x in range(0,len(command) + 1):
            self.device.ws.recv()
        result = self.device.ws.recv()
        print("###########")
        print(result)
        print("###########")
        return json.loads(result)

class device:
    def __init__(self, info, callables):
        self.info = info
        for callable in callables:
            exec("self." + callable + " = callableFunction('" + callable + "', callables[callable], self)")
        self.connect()

    def disconnect(self):
        self.ws.close()

    def connect(self):
        self.ws = websocket.WebSocket()
        self.ws.connect("ws://" + self.info['ip'] + ":8266")
        self.ws.recv()
        self.ws.send("OneIoT\n")
        self.ws.recv()
        self.ws.send("import user, json\r\n")
        for x in range(0,len("import user, json") + 2):
            self.ws.recv()

    def upload(self, source, destination):
        self.disconnect()
        webrepl_cli.main('OneIoT', '192.168.4.7:' + destination, 'put', src_file=source)
        self.connect()

    def reset(self):
        self.ws.send("import machine\r\n")
        self.ws.send("machine.reset()\r\n")
        self.disconnect()
        self.connect()
