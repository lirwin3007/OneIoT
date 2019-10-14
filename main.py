import Pyro4
from Pyro4.util import SerializerBase

from Device import Device
from DeviceManager import DeviceManager

def device_to_dict(device):
    result = device.__dict__
    #result['__class__'] = 'Device.Device'
    return result

def dict_to_device(class_name, dictionary):
    return Device(dictionary['id'], dictionary['ip'])

def main():
    Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')
    Pyro4.config.SERIALIZER = 'pickle'
    #SerializerBase.register_class_to_dict(Device, device_to_dict)
    #SerializerBase.register_dict_to_class('Device.Device', dict_to_device)
    Pyro4.Daemon.serveSimple(
            {
                DeviceManager: "oneIoT.device_manager"
            })

if __name__=="__main__":
    main()
