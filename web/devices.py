import os, configparser, json
import requests

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
        arg_list = {self.args[i]:argv[i] for i in range(0, len(argv))}
        result = requests.post('http://' + self.device.info['ip'] + '/' + self.name, json=arg_list)
        return json.loads(result.content.decode("utf-8"))

class device:
    def __init__(self, info, callables):
        self.info = info
        for callable in callables:
            exec("self." + callable + " = callableFunction('" + callable + "', callables[callable], self)")
