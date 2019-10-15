from Device import Device

import os, json, configparser

class DeviceManager:

    def __init__(self):
        self._devices = {}
        self._ssid = "OneIoT"
        self._wpaPsk = "OneIoTPass"

        self._device_path = os.path.expanduser('~') + '/.oneIot'
        if not os.path.isdir(self._device_path):
            os.mkdir(self._device_path)
        if not os.path.isdir(self._device_path + '/devices'):
            os.mkdir(self._device_path + '/devices')

        config = configparser.ConfigParser()
        for directory in [f.path for f in os.scandir(self._device_path + '/devices') if f.is_dir()]:
            config.read(directory + '/config.ini')
            config = {x:config['info'][x] for x in config['info']}
            new_device = Device(config)
            self._devices[new_device.id] = new_device

    def add_device(self, id, port):
        if id not in self._devices:
            ipEnd = 1
            ipFound = True
            while ipFound:
                ipFound = False
                for device in self._devices:
                    if device.ip == '192.168.4.' + str(ipEnd):
                        ipFound = True
                ipEnd += 1
            device_path = self._device_path + '/devices/' + device.id
            if not os.path.isdir(device_path):
                os.mkdir(device_path)
            device = Device({'id': id, 'ip': '192.168.4.' + str(ipEnd), 'device_path': device_path})
            device.flashTTY(port)
            self._devices[device.id] = device
        else:
            raise Exception("Device id already taken")

    def init_device(self, id, port):
        if id in self._devices:
            device = self._devices[id]
            device.connectTTY(port)
            print(device.sendTTY('import webrepl_setup'))
            print(device.sendTTY('E'))
            print(device.sendTTY('secret'))
            print(device.sendTTY('secret'))
            print(device.sendTTY('n'))
            print(device.sendTTY('boot = open("boot.py", "wb")'))
            print(device.sendTTY('boot.write("import network\\n")'))
            print(device.sendTTY('boot.write("wlan=network.WLAN(network.STA_IF)\\n")'))
            print(device.sendTTY('boot.write("wlan.active(True)\\n")'))
            print(device.sendTTY('boot.write("wlan.connect(\'' + self._ssid + '\', \'' + self._wpaPsk + '\')\\n")'))
            print(device.sendTTY('boot.write("wlan.ifconfig((\'' + device.ip + '\',\'255.255.255.0\',\'192.168.4.1\',\'8.8.8.8\'))\\n")'))
            print(device.sendTTY('boot.write("import webrepl\\n")'))
            print(device.sendTTY('boot.write("webrepl.start()\\n")'))
            print(device.sendTTY('boot.close()'))
            print(device.sendTTY('user = open("user.py", "wb")'))
            print(device.sendTTY('user.write("pass")'))
            print(device.sendTTY('user.close()'))
            device.resetTTY()
            device.disconnectTTY()
            device.save()
        else:
            raise Exception("Unknown device id")


    def get_device(self, device_id):
        if device_id not in self._devices:
            raise Exception("Device id not found")
        else:
            return self._devices[device_id]

## Testing

#dm = DeviceManager()

## Setup a device
#dm.add_device('test', 'ttyUSB0')
#input("Remove jumpers, reset & press enter")
#dm.init_device('test', 'ttyUSB0')

## Retreive the device and connect to it
#device = dm.get_device('test')
#device.connect()

## Upload a file to the device
#device.upload("/home/pi/.oneIot/devices/test/user.py", "user.py")

## Run a test routine
#print(device.multiply(5,2))
#print(device.check_if_equal(5,5))
#print(device.make_dict())

## Disconnect from the device
#device.disconnect()
