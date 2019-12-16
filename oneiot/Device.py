import json
import configparser, esptool, serial, time, re, os

import socket

DEVICE_CONNECTED = 0
DEVICE_NOT_CONNECTED = 1

class Callable:

    def __init__(self, command, device):
        self.command = command
        self.device = device

    def __call__(self, *argv):
        return self.device.send(self.command, list(argv))

class Device:
    """
    A device represents a physical OneIoT device.

    The class also contains methods corrisponding to any methods on the device
    that it represents. These can be called like normal methods, and return
    the value that the device returns.
    """
    def __init__(self, config, new_device=False):
        self.id = config['id']
        self.ip = config['ip'] if 'ip' in config else None
        self.device_path = config["device_path"]
        self.status = DEVICE_NOT_CONNECTED
        self._ttyPort = None
        if not new_device:
            self.refreshMethods()
        else:
            self.callables = []

    def _send_to_core(self, command, args):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(("localhost", 1102))
            command_string = command
            for arg in args:
                command_string += "\n" + (json.dumps(arg) if isinstance(arg, list) else str(arg))
            sock.sendall(bytes(command_string, 'ascii'))
            result = str(sock.recv(1024), 'ascii')
            return result

    @property
    def connected(self):
        """
        Get the connected state of the device.

        :rtype: Boolean
        """
        return json.loads(self._send_to_core("connect_test", [self.id]))

    @property
    def code(self):
        """
        Get the code currently on the device.

        :rtype: String
        """
        if os.path.exists(self.device_path + "/user.py"):
            return open(self.device_path + "/user.py").read()
        else:
            return ""

    def refreshMethods(self):
        self.callables = json.load(open(self.device_path + "/device.json"))
        for callable in self.callables:
            setattr(self, callable, Callable(callable, self))
            #exec("self." + callable + " = callableFunction('" + callable + "', self.callables[callable], self)")

    def save(self):
        """
        Save the device to be autoloaded by DeviceManager at next instantiation.
        """
        config = configparser.ConfigParser()
        config['info'] = { 'id': self.id,
                           'ip': self.ip,
                           'device_path': self.device_path }
        with open(self.device_path + '/config.ini', 'w+') as configfile:
            config.write(configfile)
        with open(self.device_path + '/device.json', 'w+') as devicefile:
            devicefile.write("[]");

    def send(self, command, args):
        result = self._send_to_core("send_to_device", [self.id, command, args])

        try:
            result = json.loads(result.split("\r\n")[0])
        except:
            raise Exception("\n\n~~ Remote Device Error ~~\n\n" + result)

        return result

    def flashTTY(self, port):
        """
        Flash the device with OneIoT firmware over a TTY port.

        :param port: port that the device is plugged into (e.g. /dev/TTYUSB0)
        :type port: String
        """
        esptool.main(custom_commandline=['--port', '/dev/' + port, 'erase_flash'])
        esptool.main(custom_commandline=['--port', '/dev/' + port, 'write_flash', '-z', '0x1000', 'esp-32-img.bin'])

    def connectTTY(self, port):
        """
        Connect to a OneIoT device over a TTY port.

        :param port: port that the device is plugged into (e.g. /dev/TTYUSB0)
        :type port: String
        """
        self.ser = serial.Serial('/dev/' + port, 115200, timeout=1)
        self._ttyPort = port
        self.receiveTTY()

    def receiveTTY(self, timeout=500):
        """
        Receive from a OneIoT device over a TTY port

        :param timeout: timeout waiting for a response (ms)
        :type timeout: Integer
        :rtype: ByteString
        """
        if self._ttyPort != None:
            result = b''
            addition = ' '
            startTime = int(round(time.time() * 1000))
            while addition != b'' and int(round(time.time() * 1000)) < startTime + timeout:
                addition = self.ser.read()
                result += addition
            return result
        else:
            raise Exception("No TTY Connection")

    def sendTTY(self, command):
        """
        Send to a OneIoT device over a TTY port and return the result.

        :param command: command to send to the OneIoT device
        :type command: String
        :rtype: ByteString
        """
        if self._ttyPort != None:
            self.ser.writelines([str.encode(command) + b"\r\n"])
            self.ser.readline()
            return self.ser.readline()[:-2].decode('utf-8')
        else:
            raise Exception("No TTY Connection")

    def disconnectTTY(self):
        """
        Disconnect from a OneIoT device over a TTY port.
        """
        if self._ttyPort != None:
            self.ser.close()
            self._ttyPort = None
        else:
            raise Exception("No TTY Connection")

    def resetTTY(self):
        """
        Reset a OneIoT device over a TTY port.
        """
        if self._ttyPort != None:
            self.sendTTY("import machine")
            self.sendTTY("machine.reset()")
            port = self._ttyPort
            self.disconnectTTY()
            self.connectTTY(port)
        else:
            raise Exception("No TTY Connection")

    def disconnect(self):
        """
        Disconnect from a OneIoT device
        """
        self._send_to_core("disconnect", [self.id])

    def connect(self):
        """
        Connect to a OneIoT device
        """
        result = self._send_to_core("connect", [self.id, self.ip]).split("\n")

        if not json.loads(result[0]):
            raise Exception(result[1])
        else:
            self.status = DEVICE_CONNECTED

    def reset(self):
        """
        Reset a OneIoT device
        """
        self._send_to_core("reset", [self.id, self.ip])

    def uploadString(self, stringSource, destination):
        """
        Upload a given string as a file to a OneIoT device.

        :param stringSource: Source string
        :type stringSource: String
        :param destination: Destination file (absolute file path)
        :type destination: String
        """
        open(self.device_path + "/user.py", "w").write(stringSource)
        self.upload(self.device_path + "/user.py", destination)

    def upload(self, source, destination):
        """
        Upload a file to a OneIoT device.

        :param source: Source file (absolute file path)
        :type source: String
        :param destination: Destination file (absolute file path)
        :type destination: String
        """
        # Parse the user's code for routines
        all_routines = re.findall("def .*", open(source).read())
        callables = {}
        for routine in all_routines:
            routine_name = routine[routine.index("def ")+4:routine.index("(")].strip()
            args = routine[routine.find("(") + 1:routine.find(")")]
            callables[routine_name] = args.split(",")
            callables[routine_name] = [x.strip() for x in callables[routine_name]]
            if callables[routine_name] == ['']:
                callables[routine_name] = []

        # Update the device's json file
        open(self.device_path + '/device.json', 'w+').write(json.dumps(callables))
        self.refreshMethods()

        # Upload the file
        self._send_to_core("upload", [self.id, self.ip, source, destination])
