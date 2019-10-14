import sys
import Pyro4
import Pyro4.util

sys.excepthook = Pyro4.util.excepthook

device_manager = Pyro4.Proxy("PYRONAME:oneIoT.device_manager")
device_manager.add_device('hi')
print(device_manager.get_device('hi'))
